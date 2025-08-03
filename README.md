---

## Gmail to Google Drive Uploader

This project automates the process of downloading email attachments from a Gmail inbox and uploading them to a specified Google Drive folder — all done securely and hands-free.

It is especially useful for recurring daily or hourly reports, transaction logs, or any automated system that sends files via email.

With GitHub Actions integration, the script can run on a schedule, or you can manually trigger it from the GitHub interface — no local execution required after setup!

---

## Project Structure

```
gmail_drive_uploader/
│
├── gmail_to_drive.py               # Main script that connects to Gmail and uploads attachments to Google Drive
├── credentials.json                # OAuth 2.0 credentials downloaded from Google Cloud Console (Desktop App type)
├── token.json                      # Automatically generated token after first successful OAuth login (stores access/refresh tokens)
├── .env                            # Environment variables file containing sensitive data like Gmail and Drive credentials (exclude from git)
├── requirements.txt                # List of Python dependencies needed to run the script
│
├── .github/                        # Directory for GitHub-related configurations
│   └── workflows/               
│       └── gmail_drive_upload.yml  # GitHub Actions CI workflow to automate runs (e.g., scheduled or manual upload jobs)
│
├── .gitignore                      # Specifies which files/folders Git should ignore (e.g., `.env`, `token.json`, etc.)
└── README.md                       # Project documentation with setup instructions, usage, and troubleshooting

```

## Features

* **IMAP-based Gmail filter**: Only fetches emails from a specific sender/subject.
* **Attachment scanner**: Downloads only supported files (e.g., `.csv`, `.xlsx`).
* **Drive integration**: Uploads to a target Google Drive folder using Drive API.
* **Duplicate handling**: Automatically skips already-uploaded files.
* **Terminal logging**: Prints helpful logs for success, skip, or errors.

---

## Prerequisites

* Python 3.10+
* Google Account with 2FA enabled
* Gmail App Password
* Google Cloud Project with Drive API enabled

---

## Step-by-Step Setup Guide

---

### 1. Install Python (if not already installed)

* Download from: [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 2. Clone the Repository

```bash
git clone https://github.com/prantonia/gmail-drive-uploader.git
cd gmail_drive_uploader
```

---

### 3. Set Up Virtual Environment (Recommended)

```bash
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, run:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib imaplib2 python-dotenv
```

---

### 5. Gmail Configuration

#### a. Enable IMAP

1. Go to Gmail → **Settings** → **See all settings**
2. Navigate to **Forwarding and POP/IMAP**
3. Enable **IMAP access** → Save changes

#### b. Create App Password (not your normal password)

1. Visit: [https://myaccount.google.com/security](https://myaccount.google.com/security)
2. Under **2-Step Verification**, click **App Passwords**
3. Select app: `Mail`, device: `Windows Computer`
4. Copy the generated 16-digit password

Use this in `.env` as your `EMAIL_PASSWORD`.

---

### 6. Google Drive API Setup

#### a. Create a Google Cloud Project

* Go to: [https://console.cloud.google.com/](https://console.cloud.google.com/)
* Create a new project

#### b. Enable Google Drive API

* Navigate to **APIs & Services** → **Library**
* Search and enable: `Google Drive API`

#### c. Create OAuth Credentials

1. Go to **Credentials** → **Create Credentials** → **OAuth Client ID**
2. Choose **Desktop App**
3. Download `credentials.json` into your project directory

> Keep this file safe. Do NOT commit it to GitHub.

---

### 7. Setup `.env` File

Create a `.env` file at the root of your project with the following:

```ini
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_character_app_password
EMAIL_SENDER_FILTER=sender@domain.com
GDRIVE_FOLDER_ID=your_google_drive_folder_id
```

**Get your `GDRIVE_FOLDER_ID`:**

* Right-click on the destination folder in Drive → "Get Link"
* Copy the string after `/folders/` in the URL.
    Like this: https://drive.google.com/drive/folders/xxxxxxxxxxxxxxxxxxxxxx

---

### 8. Run the Script

```bash
python gmail_to_drive.py
```

On first run:

* A browser window opens for Google OAuth login
* `token.json` will be saved for future runs

---

## Automation (Optional)

### Using GitHub Actions for Hourly Automation

* Set up a GitHub Action to trigger every hour using:

```yaml
on:
  schedule:
    - cron: '0 * * * *'  # every hour on the hour
```

Ensure your script runs headlessly and uses refresh tokens instead of browser login.

---

## Regenerate `requirements.txt`

```bash
pip freeze > requirements.txt
```

---

## Troubleshooting

| Issue                    | Solution                                                         |
| ------------------------ | ---------------------------------------------------------------- |
| **OAuth browser error**  | Replace `run_console()` with `run_local_server()` in your script |
| **App password fails**   | Ensure 2FA is enabled and correct password used                  |
| **Drive upload fails**   | Recheck `GDRIVE_FOLDER_ID` and MIME types                        |
| **No attachments found** | Verify Gmail filters (sender/subject) are correct                |

---

## Cleanup & Security

* Add `credentials.json`, `token.json`, `.env` to your `.gitignore`
* Never upload your secrets to GitHub

```gitignore
credentials.json
token.json
.env
```

---

## Technologies Used

* Gmail IMAP (`imaplib2`)
* Google Drive API (`google-api-python-client`)
* OAuth 2.0 Auth (`google-auth`)
* Environment config (`python-dotenv`)

---

## Credits

* Inspired by real-world automation needs.

---