<div align="center">

# GitHub-ContriBot
**Automated GitHub contribution lifecycle bot**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

![GitHub-ContriBot Banner](assets/banner.png)

</div>

## Overview

GitHub-ContriBot is a GitHub Actions based automation project that performs a complete contribution lifecycle inside your repository.

Each successful bot cycle can:

- create a new issue
- assign the issue to your account
- create a temporary update branch from `main`
- modify `contribution_log.txt`
- commit and push the branch
- create a pull request into `main`
- assign the pull request to your account
- submit a review
- merge the pull request
- close the issue through the PR body
- delete the temporary branch

The current design is built specifically to avoid workflow loops. The automation runs only from scheduled triggers and manual workflow dispatches. It does not run on `push`, so bot-created merges do not recursively trigger new runs.

## Architecture

The project has three main parts:

- `Automator.py`: the Python automation script
- `.github/workflows/main.yml`: the GitHub Actions workflow
- `.bot_state.json`: the persistent daily quota state

The workflow checks out the repository, installs dependencies, configures git, and runs `Automator.py`.

The Python script is responsible for:

- tracking the current day's quota
- deciding whether another cycle should run
- creating the issue / branch / PR / review / merge sequence
- updating the state after a successful cycle

## Daily Quota System

The bot no longer relies on fixed morning and night execution windows.

Instead, it uses a daily random target:

- at the start of a new UTC day, the bot selects a random `daily_target` from `1` to `25`
- each workflow run performs at most one complete contribution lifecycle
- after each successful lifecycle, the bot increments `completed`
- once `completed == daily_target`, later runs for that day exit without making changes

Example:

```json
{
  "date": "2026-03-19",
  "daily_target": 17,
  "completed": 4
}
```

This means the bot will continue producing one new issue -> PR -> merge cycle per scheduled run until it reaches `17` for that day.

## Workflow Behavior

The GitHub Actions workflow is configured with:

- `schedule`
- `workflow_dispatch`
- `concurrency`

### Why `concurrency` matters

It prevents two bot runs from executing at the same time. This avoids branch collisions, duplicated PR creation, and quota race conditions.

### Why there is no `push` trigger

This is the key fix for the looping problem.

When the bot merges a pull request into `main`, that merge creates a new commit in the repository. If the workflow listened to `push`, the merge would trigger the bot again and create an automation loop.

By using only scheduled and manual triggers:

- merges to `main` do not trigger the bot
- only the scheduler or a manual run can start a new cycle

## Full Bot Lifecycle

During one successful execution, the bot performs the following:

1. Sync local checkout to the latest `main`
2. Read `.bot_state.json`
3. If it is a new day, generate a new random target between `1` and `25`
4. If the day's quota is already complete, exit cleanly
5. Create a fresh branch such as `update-20260319093000-5`
6. Append a new entry to `contribution_log.txt`
7. Commit the change
8. Push the branch to GitHub
9. Create an issue
10. Assign that issue to the configured GitHub user
11. Create a PR from the temporary branch to `main`
12. Assign the PR to the configured user
13. Submit a review
14. Merge the PR into `main`
15. Delete the temporary branch
16. Update `.bot_state.json` with the new completed count

## Review Behavior

GitHub does not allow a user to approve their own pull request.

Because of that, the bot uses this logic:

- first it tries to submit an approval review
- if GitHub rejects it because the PR author and reviewer are the same account, it falls back to a review comment

This keeps the workflow running successfully in a single-account setup.

If you want actual approval reviews, you need:

- a second GitHub account, or
- a separate token belonging to another reviewer identity

## Setup Guide

### 1. Fork or Clone the Repository

Create your own copy of this repository on GitHub.

### 2. Ensure the Default Branch Is `main`

The bot opens PRs against `main` and synchronizes from `main`.

If your default branch is not `main`, update the branch constant in `Automator.py`.

### 3. Enable GitHub Actions

Open the repository on GitHub and make sure Actions are enabled.

### 4. Add Repository Secrets

Go to:

`Settings -> Secrets and variables -> Actions`

Add these secrets:

- `PAT_TOKEN`
- `COMMIT_USERNAME`
- `COMMIT_EMAIL`

### 5. Secret Details

#### `PAT_TOKEN`

Use a GitHub Personal Access Token that has enough permission to:

- read and write repository contents
- create and manage issues
- create and merge pull requests

For a classic token, `repo` is the important scope. If you use a fine-grained token, give it equivalent repository permissions.

#### `COMMIT_USERNAME`

This must be your GitHub username. The bot uses it for issue assignment and PR assignment.

#### `COMMIT_EMAIL`

This should be an email address linked to your GitHub account. If the email is not linked to your account, merged commits may not show correctly in your contribution graph.

### 6. Push the Workflow to the Default Branch

Scheduled GitHub Actions workflows run only when the workflow file exists on the repository's default branch.

If you build changes in `Version-2.0` or any other branch, you must merge them into `main` before expecting scheduled runs to start automatically.

## Manual Testing

To test the automation immediately:

1. Open your repository on GitHub
2. Go to the `Actions` tab
3. Select the `Daily Contribution` workflow
4. Click `Run workflow`

Expected result for a successful run:

- one new issue is created
- one new PR is created
- the PR is merged into `main`
- the state file is updated
- the workflow run shows a green check mark

## Scheduled Execution

The workflow is currently configured to run hourly.

That means:

- GitHub creates a new workflow run on the cron schedule
- each run checks whether the daily quota is already complete
- if quota is available, one new lifecycle is executed
- if quota is already met, the run exits without creating more activity

So the Actions tab may show many runs in a day, but only some of them will create a new PR and merge depending on the current quota state.

## Contribution Graph Expectations

This bot is designed to create contribution-related activity such as:

- merged commits on the default branch
- issues
- pull requests
- review comments or approval attempts

Whether those appear on your GitHub contribution graph depends on GitHub's contribution rules, your account email configuration, and whether the repository qualifies for profile contributions.

## Customization

You can adjust the bot behavior by changing:

- the daily quota range in `Automator.py`
- the workflow schedule in `.github/workflows/main.yml`
- the base branch name
- the labels applied to issues and PRs
- the file changed in each cycle

## Files

- `Automator.py`: main automation logic
- `.github/workflows/main.yml`: scheduler and workflow definition
- `.bot_state.json`: persistent state for quota tracking
- `contribution_log.txt`: file updated by the bot
- `requirements.txt`: Python package dependencies

## Troubleshooting

### The workflow does not appear automatically in Actions

Check these points:

- the workflow file is present on `main`
- Actions are enabled in the repository
- the workflow has already been merged into the default branch

### Manual run works, but schedule does not run immediately

This is normal. Scheduled GitHub workflows are not always visible instantly after the workflow is merged into the default branch. Wait for the next cron interval.

### The review step fails

If you are using only one GitHub account, GitHub will not allow self-approval of PRs. The bot now handles this by falling back to a review comment.

### The bot is not showing contributions on the profile graph

Check:

- `COMMIT_EMAIL` matches an email linked to your GitHub account
- commits are being merged into the default branch
- issues and PRs are being created in a repository that counts toward profile contributions

## License

This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for full details.

## Author

**Pareekshith Palat**

- **GitHub**: [PareekshithPalat](https://github.com/PareekshithPalat)
- **Email**: pareekshithpalat@gmail.com

---

Use this automation responsibly and verify that the configured permissions, repository settings, and contribution expectations match your GitHub setup.
