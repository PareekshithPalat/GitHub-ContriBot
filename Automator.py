"""
Author : Pareekshith1 {Pareekshith.P}
"""
import json
import os
import random
from datetime import datetime, timezone

import github
from git import Repo
from github import Github

REPO_PATH = os.getcwd()
BASE_BRANCH = "main"
FILE_TO_UPDATE = "contribution_log.txt"
STATE_FILE = ".bot_state.json"
LABELS = ["updation"]


def get_random_review():
    comments = [
        "Reviewed the automated update. Approved.",
        "Change looks valid and ready to merge.",
        "Verified the generated update. Approving.",
        "Checked the update branch and approved the PR.",
        "Automated review completed successfully.",
    ]
    return random.choice(comments)


def state_file_path():
    return os.path.join(REPO_PATH, STATE_FILE)


def load_state():
    path = state_file_path()
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(state):
    with open(state_file_path(), "w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
        handle.write("\n")


def get_today_state():
    today = datetime.now(timezone.utc).date().isoformat()
    state = load_state()
    if state.get("date") != today:
        state = {
            "date": today,
            "daily_target": random.randint(1, 25),
            "completed": 0,
        }
    return state


def sync_main_branch(local_repo):
    origin = local_repo.remote(name="origin")
    local_repo.git.checkout(BASE_BRANCH)
    origin.fetch(BASE_BRANCH)
    local_repo.git.reset("--hard", f"origin/{BASE_BRANCH}")
    return origin


def commit_state(local_repo, origin, state):
    save_state(state)
    local_repo.index.add([STATE_FILE])
    if not local_repo.is_dirty(untracked_files=True):
        return
    local_repo.index.commit(
        f"bot-state: {state['date']} {state['completed']}/{state['daily_target']}"
    )
    origin.push(BASE_BRANCH)


def create_cycle_change(local_repo, cycle_number):
    timestamp = datetime.now(timezone.utc).isoformat()
    with open(os.path.join(REPO_PATH, FILE_TO_UPDATE), "a", encoding="utf-8") as handle:
        handle.write(
            f"\nContribution cycle {cycle_number} executed at {timestamp}"
        )
    local_repo.index.add([FILE_TO_UPDATE])
    local_repo.index.commit(f"Contribution cycle {cycle_number}: {timestamp}")


def delete_remote_branch(remote_repo, branch_name):
    ref = remote_repo.get_git_ref(f"heads/{branch_name}")
    ref.delete()


def run_cycle(local_repo, remote_repo, gh_username, cycle_number):
    branch_stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    branch_name = f"update-{branch_stamp}-{cycle_number}"
    local_repo.git.checkout("-b", branch_name)
    print(f"Switched to branch: {branch_name}")

    create_cycle_change(local_repo, cycle_number)

    origin = local_repo.remote(name="origin")
    print(f"Pushing branch {branch_name} to remote...")
    origin.push(refspec=f"{branch_name}:{branch_name}")

    issue_title = f"Task for {datetime.now(timezone.utc).strftime('%Y-%m-%d')} #{cycle_number}"
    issue_body = "This issue is created automatically to track contribution activity."
    issue = remote_repo.create_issue(
        title=issue_title,
        body=issue_body,
        assignee=gh_username,
        labels=LABELS,
    )
    print(f"Created issue #{issue.number}")

    pr_title = f"Feature: Contribution cycle {cycle_number}"
    pr_body = (
        "This PR contains an automated contribution update.\n\n"
        f"Closes #{issue.number}"
    )
    pr = remote_repo.create_pull(
        title=pr_title,
        body=pr_body,
        base=BASE_BRANCH,
        head=branch_name,
    )
    pr.add_to_assignees(gh_username)
    pr.add_to_labels(*LABELS)
    print(f"Created PR #{pr.number}: {pr.html_url}")

    pr.create_review(body=get_random_review(), event="APPROVE")
    print(f"Approved PR #{pr.number}")

    merge_status = pr.merge(
        merge_method="squash",
        commit_message=f"Merged automated contribution PR #{pr.number}",
    )
    if not merge_status.merged:
        raise RuntimeError(f"Failed to merge PR #{pr.number}: {merge_status.message}")

    print(f"PR #{pr.number} merged successfully")

    delete_remote_branch(remote_repo, branch_name)
    print(f"Deleted remote branch {branch_name}")

    local_repo.git.checkout(BASE_BRANCH)
    local_repo.git.branch("-D", branch_name)


def main():
    token = os.environ.get("PAT_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    gh_username = os.environ.get("GH_USERNAME")

    if not all([token, repo_name, gh_username]):
        raise RuntimeError("PAT_TOKEN, GITHUB_REPOSITORY, and GH_USERNAME must be set.")

    client = Github(auth=github.Auth.Token(token))
    remote_repo = client.get_repo(repo_name)
    local_repo = Repo(REPO_PATH)
    origin = sync_main_branch(local_repo)

    state = get_today_state()
    print(
        f"Daily target: {state['daily_target']} | Completed today: {state['completed']}"
    )

    if state["completed"] >= state["daily_target"]:
        print("Daily quota already met. Exiting.")
        commit_state(local_repo, origin, state)
        return

    cycle_number = state["completed"] + 1
    run_cycle(local_repo, remote_repo, gh_username, cycle_number)

    origin = sync_main_branch(local_repo)
    state["completed"] = cycle_number
    commit_state(local_repo, origin, state)
    print(
        f"Updated daily state: {state['completed']}/{state['daily_target']} completed"
    )


if __name__ == "__main__":
    main()
