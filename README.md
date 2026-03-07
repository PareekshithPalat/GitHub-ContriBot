![GitHub-ContriBot Banner](assets/banner.png)

<div align="center">

# GitHub-ContriBot
**Enterprise-Grade Contribution Lifecycle Automation**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

## Overview

GitHub-ContriBot is a high-performance automation utility designed to manage and optimize developer presence on GitHub. Unlike standard contribution bots, this system automates a **complete development lifecycle**, ensuring that your activity graph reflects authentic, multi-layered engagement including branches, commits, issues, pull requests, and peer reviews.

## Core Capabilities

The Version 2.0 engine implements a sophisticated "Lifecycle Automation" pattern for every execution sequence:

- **Branch Isolation**: Every run initializes a unique, timestamped branch (e.g., `contribution-20240308...`) to maintain repository integrity.
*   **Contribution Scale**: Generates a random number of commits (**1 to 20**) per run to simulate varying levels of daily project work.
- **Issue Management**: Automatically generates a project tracking issue for each run, assigns it to your account, and applies custom labels.
- **Pull Request Automation**: Orchestrates a PR linking the branch to `main`, complete with "Closes #Issue" syntax for automatic tracking.
- **Automated Interaction**: Posts randomized, professional code review comments to the PR before finalizing.
- **Auto-Merge**: Finalizes the lifecycle by merging the PR into the production branch and cleaning up.

## Strict Scheduling

To ensure your activity aligns with professional working hours, the system maintains a strict temporal lock:

- **Execution Windows**: The bot is programmed to execute only during two specific windows:
    - **10:00 AM IST** (04:30 UTC)
    - **09:00 PM IST** (15:30 UTC)
- **Synchronized Cron**: The integrated GitHub Actions workflow is precision-tuned to trigger exactly at these intervals.

## Setup & Implementation

Follow these steps to deploy the GitHub-ContriBot enterprise solution to your account:

### 1. Preparation
1.  **Fork** this repository to your GitHub profile.
2.  Enable **GitHub Actions** in the "Actions" tab of your fork.

### 2. Authentication Configuration (Crucial)
To permit the bot to perform PR merges and reviews on your behalf, a Personal Access Token (PAT) is required.

1.  Generate a **Personal Access Token (Classic)** at [GitHub Settings](https://github.com/settings/tokens).
2.  Select the following scopes:
    -   `repo` (Full control of repositories)
    -   `workflow` (Update GitHub Action workflows)
3.  Navigate to your repository **Settings > Secrets and variables > Actions**.
4.  Add the following **Repository Secrets**:
    -   `PAT_TOKEN`: Paste your generated token here.
    -   `COMMIT_USERNAME`: Your GitHub username.
    -   `COMMIT_EMAIL`: Your GitHub email address.

### 3. Automated Deployment
Once the secrets are configured, the bot will automatically trigger based on the defined schedule. No further manual intervention is required.

## Configuration

Custom parameters can be adjusted in `Automator.py`:

| Parameter | Location | Description |
| :--- | :--- | :--- |
| Commit Range | `random.randint(1, 20)` | Controls the minimum and maximum commits per session. |
| Time Slots | `["04:30", "15:30"]` | Defines the allowed UTC execution windows. |
| Labels | `labels=["updation"]` | Sets the default labels for issues and PRs. |

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for full details.

## Author

**Pareekshith Palat**
-   **GitHub**: [@Pareekshith1](https://github.com/Pareekshith1)
-   **Email**: [Your Email Here]

---
*Disclaimer: Use this tool responsibly. It is designed for environment testing and profile maintenance.*
