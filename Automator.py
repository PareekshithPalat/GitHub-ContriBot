''' 
Author : Pareekshith1 {Pareekshith.P} 
'''
import os
import random
import sys
import time
from datetime import datetime
from git import Repo
import github
from github import Github

# Configuration
REPO_PATH = os.getcwd()
FILE_TO_UPDATE = "contribution_log.txt"

def get_random_comment():
    comments = [
        "Great changes! LGTM.",
        "Looks good to me. Ready to merge.",
        "Nice work on this update.",
        "Everything looks correct. Good job!",
        "Verified the changes, they look solid.",
        "Excellent improvements. Approved.",
        "Clean code, thanks for the contribution.",
        "This is exactly what was needed."
    ]
    return random.choice(comments)

def main():
    token = os.environ.get("PAT_TOKEN")
    repo_name = os.environ.get("GITHUB_REPOSITORY")
    gh_username = os.environ.get("GH_USERNAME")

    if not all([token, repo_name, gh_username]):
        print("Error: GITHUB_TOKEN, GITHUB_REPOSITORY, and GH_USERNAME must be set.")
        return

    g = Github(auth=github.Auth.Token(token))
    remote_repo = g.get_repo(repo_name)
    local_repo = Repo(REPO_PATH)

    # 1. Create a unique branch
    now_str = datetime.now().strftime('%Y%m%d%H%M%S')
    branch_name = f"contribution-{now_str}"
    new_branch = local_repo.create_head(branch_name)
    new_branch.checkout()
    print(f"Switched to new branch: {branch_name}")

    # 2. Make changes and commit
    num_commits = random.randint(1, 7) 
    print(f"Generating {num_commits} commits.")

    for i in range(num_commits):
        with open(os.path.join(REPO_PATH, FILE_TO_UPDATE), "a") as f:
            f.write(f"\nContribution {i+1} on {datetime.now()}")
        
        local_repo.index.add([FILE_TO_UPDATE])
        local_repo.index.commit(f"Contribution {i+1}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 3. Push the branch
    print(f"Pushing branch {branch_name} to remote...")
    origin = local_repo.remote(name='origin')
    origin.push(branch_name)

    # 4. Create an issue and assign to user
    print("Creating issue...")
    issue_title = f"Task for {datetime.now().strftime('%Y-%m-%d')}"
    issue_body = "This issue is created automatically to track daily contributions."
    issue = remote_repo.create_issue(title=issue_title, body=issue_body, assignee=gh_username, labels=["updation"])
    print(f"Created issue #{issue.number} and assigned to {gh_username}")

    # 5. Create PR
    print("Creating Pull Request...")
    pr_title = f"Feature: Contribution {datetime.now().strftime('%Y-%m-%d')}"
    pr_body = f"This PR addresses the work for today.\n\nCloses #{issue.number}"
    pr = remote_repo.create_pull(title=pr_title, body=pr_body, base="main", head=branch_name)
    print(f"Created PR #{pr.number}: {pr.html_url}")

    # 5b. Assign to user and add labels
    pr.add_to_assignees(gh_username)
    pr.add_to_labels("updation")
    print(f"Assigned PR #{pr.number} to {gh_username} with 'updation' label")

    # Wait a bit for GitHub to process
    time.sleep(5)

    # 6. Make a random review/comment
    print("Submitting automated comment...")
    pr.create_issue_comment(get_random_comment())
    print("Comment submitted.")

    # 7. Merge the PR
    print("Merging PR...")
    merge_status = pr.merge(merge_method="squash", commit_message=f"Merged automated contribution PR #{pr.number}")
    if merge_status.merged:
        print(f"PR #{pr.number} merged successfully!")
    else:
        print(f"Failed to merge PR #{pr.number}: {merge_status.message}")

if __name__ == "__main__":
    main()
