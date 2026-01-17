# LeetCode Streak Bot 🤖

[![Workflow Status](https://github.com/Kings-man-6969/leetcode-bot/actions/workflows/streak.yml)

A GitHub Actions-powered bot that automatically submits solved LeetCode problems to **maintain your daily streak**.

---

## Features

- Automatically submits a **random solved problem** from a predefined list.
- Uses **GitHub Secrets** for secure authentication (no passwords in code).
- Fully automated with **daily scheduling** via GitHub Actions.
- Logs submissions and cookie validation in GitHub Actions workflow.

---

## Setup Instructions

### 1. Create a Repository
1. Create a **private repository** on GitHub.  
2. Clone or open it in **GitHub Codespaces**.

### 2. Add Your Script
- Upload `leetcode_bot.py` to the repository.  
- Add `.github/workflows/streak.yml` for the GitHub Actions workflow.

### 3. Add GitHub Secrets
Go to **Settings → Secrets → Actions → New repository secret** and add:

| Secret Name        | Value                                  |
|-------------------|---------------------------------------|
| `LEETCODE_SESSION` | Your LeetCode session cookie           |
| `CSRFTOKEN`        | Your LeetCode CSRF token               |

> ⚠️ Do **not** share these cookies publicly. They give access to your account.

### 4. Configure Workflow
- Workflow is located at `.github/workflows/streak.yml`.  
- Runs **daily at 04:00 UTC** by default.  
- Can also be triggered manually via **Run workflow** in GitHub Actions.

### 5. Add Problems
- Edit `leetcode_bot.py` to include your solved problems in the `problems` list.  
- Each problem requires:
  - `slug` (LeetCode URL slug)  
  - `question_id` (internal problem ID)  
  - `solution` (Python solution code)

---

## How It Works

1. **Random Problem Selection**: Each run, the bot picks one problem from the list.  
2. **Cookie Validation**: The bot checks if your `LEETCODE_SESSION` and `CSRFTOKEN` are valid.  
3. **Submission**: Sends your Python solution to LeetCode via their submission API.  
4. **Logging**: All logs are printed in GitHub Actions for verification.

---

## Running Locally
```
pip install requests
python leetcode_bot.py
```

## Temporarily set environment variables if testing locally:
```
set LEETCODE_SESSION=your_session_cookie
set CSRFTOKEN=your_csrf_cookie
```

Or paste cookies directly into the script for local testing.

## Security

Never commit your session cookies to the repository.

Always store them in GitHub Secrets for safety.

Keep the repository private to prevent misuse.

## Future Improvements

Randomly select from 10–20 solved problems for more natural activity.

Check submission status (Accepted / Wrong Answer / Runtime Error).

Add retries if cookies expire.

Extend to multiple languages or platforms.

## License

This project is personal use only. Do not distribute with your LeetCode cookies.
