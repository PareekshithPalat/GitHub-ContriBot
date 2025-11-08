# GitHub Contribution Bot 🤖

Automate your GitHub contribution graph with intelligent daily commits. This bot generates random contributions to keep your GitHub profile active and engaging.

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

- **Automated Daily Commits**: Random commits (1-10 per day) to maintain consistent activity
- **Customizable Schedule**: Runs continuously and checks for date changes
- **Private Repository Support**: Works seamlessly with private repos
- **Easy Configuration**: Simple path setup and execution

## 🚀 Quick Start

### Prerequisites
- Python 3.x installed
- Git configured on your system
- GitHub account

### Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/GitHub_Contributor_bot.git
   cd GitHub_Contributor_bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a private repository**
   - Go to GitHub and create a new private repository
   - Clone it to your local machine

4. **Setup the bot**
   - Copy `Automator.py` to your private repository
   - Create a text file named `updator.txt` in the same directory

5. **Configure paths**
   - Open `Automator.py` in a text editor
   - Update line 37 with your repository path:
     ```python
     repo_path = r"C:\Your\Path\To\Repository"
     ```

6. **Run the bot**
   ```bash
   python Automator.py
   ```

## 📝 How It Works

1. The bot runs continuously in the background
2. Each day, it generates a random number (1-10) of commits
3. For each commit, it appends text to `updator.txt`
4. Changes are automatically committed and pushed to GitHub
5. Your contribution graph updates accordingly

## ⚙️ Configuration

You can customize the bot by modifying these parameters in `Automator.py`:

- **Commit frequency**: Change `random.randint(1, 10)` on line 28
- **Branch name**: Modify `branch = "main"` on line 48
- **Commit message**: Edit `commit_message` on line 56

## ⚠️ Important Notes

- **Use a private repository** to keep automated commits separate from your actual work
- **Ensure Git credentials** are configured to avoid authentication prompts
- **Run as background process** for continuous operation
- This is for educational purposes; use responsibly

## 📋 Requirements

```
gitpython==3.1.30
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author

**Pareekshith P**
- GitHub: [@Pareekshith1](https://github.com/Pareekshith1)

## 🙏 Acknowledgments

Built with Python and GitPython library for seamless Git automation.

**Image Credits:**
- Before image: [Adrian Roselli](https://adrianroselli.com/wp-content/uploads/2018/02/GitHub-chart_scrollbar.png)
- After image: [Medium Article](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*1tUp8vKCZDVtNIJY6A-Ilg.png)

---

<div align="center">

**Note:** The before/after contribution chart images shown above are for reference purposes only to demonstrate the potential impact of using this bot.

Made with ❤️ for the GitHub community

</div>
