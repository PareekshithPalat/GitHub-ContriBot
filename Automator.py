''' 
Author : Pareekshith1 {Pareekshith.P} 
'''
import os
import random
import sys
from datetime import datetime
from git import Repo
from github import Github

# Configuration
REPO_PATH = os.getcwd() # Assumes script is run from root of repo
FILE_TO_UPDATE = "contribution_log.txt"
BRANCH = "main"

def git_commit(repo, message):
    try:
        repo.git.add(update=True)
        repo.index.add([FILE_TO_UPDATE])
        repo.index.commit(message)
        print(f"Committed: {message}")
    except Exception as e:
        print(f"Error committing: {e}")

def create_issue(github_token, repo_name):
    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        title = f"Automated Issue {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        body = "This is an automated issue created to increase activity."
        issue = repo.create_issue(title=title, body=body)
        print(f"Created issue: {issue.html_url}")
    except Exception as e:
        print(f"Error creating issue: {e}")

def main():
    # 1. Setup Git Repo
    try:
        repo = Repo(REPO_PATH)
    except Exception as e:
        print(f"Error initializing repo: {e}")
        return

    # 2. Determine random number of contributions
    # Range 1 to 10 commits per run
    num_commits = random.randint(1, 10) 
    print(f"Generating {num_commits} commits for today.")

    # 3. Loop and Commit
    for i in range(num_commits):
        with open(os.path.join(REPO_PATH, FILE_TO_UPDATE), "a") as f:
            f.write(f"\nCorrection {i+1} on {datetime.now()}")
        
        git_commit(repo, f"Contribution {i+1}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 4. Push changes
    # Use git command directly for push to avoid complex auth handling in python if args provided, 
    # but since we are in Actions, we rely on the Action step to push usually, 
    # OR we can try pushing here if configured.
    # ideally, in GH Actions, we just commit here, and use `ad-m/github-push-action` or `git push` in yaml.
    # But user asked for the "code" to do it.
    # Let's simplify: The script commits locally. The Workflow will push.
    # MUCH safer and standard for Actions. 
    print("Commits created locally.")

    # 5. Randomly create an issue (e.g., 20% chance)
    if random.random() < 0.2:
        token = os.environ.get("GITHUB_TOKEN")
        # We need the repo name format "user/repo"
        # Try to get it from git config or env
        repo_name = os.environ.get("GITHUB_REPOSITORY")
        
        if token and repo_name:
            print("Lucky Draw! Creating an issue...")
            create_issue(token, repo_name)
        else:
            print("Skipping issue creation: GITHUB_TOKEN or GITHUB_REPOSITORY not found.")

if __name__ == "__main__":
    main()
