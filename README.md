# GitHub Contribution Bot 🤖

Automate your GitHub contribution graph with intelligent daily commits and random issue creation. This bot runs on **GitHub Actions** to keep your profile active effortlessly.

## 📊 Before & After

<div align="center">

### Before Using Bot
![Sparse GitHub Contributions](https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fadrianroselli.com%2Fwp-content%2Fuploads%2F2018%2F02%2FGitHub-chart_scrollbar.png&f=1&nofb=1&ipt=82696987c41c0241e6bee6d06c6263e826fc498a0d79c91af05086026d6039ae)
*Minimal contribution activity*

### After Using Bot
![Active GitHub Contributions](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*1tUp8vKCZDVtNIJY6A-Ilg.png)
*Consistent daily contributions!*

</div>

## ✨ Features

- **Automated Daily Commits**: Random commits (1-10 per day) directly to the repository.
- **Random Issue Creation**: 20% chance to create a random issue to simulate deeper activity.
- **GitHub Actions Support**: Runs automatically in the cloud. No need to keep your PC on.
- **Easy Setup**: Just Fork and Enable!

## 🚀 Quick Start (GitHub Actions)

1. **Fork this repository** to your own GitHub account.
2. Go to the **Actions** tab in your forked repository.
3. If prompt appears, click **"I understand my workflows, go ahead and enable them"**.
4. The bot will now run automatically every day at 02:30 UTC.

(Optional) To trigger it immediately:
- Go to **Actions** -> **Daily Contribution**.
- Click **Run workflow**.

## 💻 Manual / Local Usage

If you prefer to run it locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/GitHub_Contributor_bot.git
   cd GitHub_Contributor_bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the bot**:
   ```bash
   python Automator.py
   ```
   *Note: For Issue creation to work locally, you must set `GITHUB_TOKEN` and `GITHUB_REPOSITORY` environment variables.*

## ⚙️ Configuration

You can customize the bot by editing `Automator.py`:

- **Commit frequency**: Change `random.randint(1, 10)` in `main()`.
- **Issue chance**: Change `if random.random() < 0.2:` (currently 20%).

## ⚠️ Important Notes

- **Educational Purpose**: This tool is for demonstration and testing.
- **Green Activity Bar**: Helps fill up your contribution graph.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source.

## 👤 Author

**Pareekshith P**
- GitHub: [@Pareekshith1](https://github.com/Pareekshith1)
