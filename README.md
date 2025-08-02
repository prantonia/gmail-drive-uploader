---

## 📤 Gmail to Google Drive Uploader

This Python script connects to a Gmail inbox, downloads attachments from specific emails, and uploads them to a designated folder in Google Drive — skipping duplicates by filename.

---

### 📁 Project Structure

```
gmail_drive_uploader/
│
├── gmail_to_drive.py          # Main script to run
├── credentials.json           # OAuth 2.0 Client ID credentials from Google
├── token.json                 # Generated after first login (OAuth token)
├── README.md                  # You're here
├── requirements.txt           # Dependency list
```

---

### ✅ Features

* Downloads attachments (CSV/XLSX) from Gmail based on filters.
* Uploads to a specific folder in Google Drive.
* **Skips upload** if the file already exists in Drive (no duplicates).
* Logs each step for transparency and debugging.

---

### ⚙️ Prerequisites

#### 1. Python 3.7+

Install Python from [https://www.python.org/downloads/](https://www.python.org/downloads/)

---

### 📦 Installation Steps

#### Step 1: Clone or Download the Project

```bash
git clone https://github.com/your-username/gmail_drive_uploader.git
cd gmail_drive_uploader
```

#### Step 2: Set Up a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

#### Step 3: Install Required Libraries

```bash
pip install -r requirements.txt
```

If `requirements.txt` is missing, install manually:

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib imaplib2 python-dotenv
```

---

### 🔐 Gmail Setup

#### Step 1: Enable IMAP in Gmail

* Go to your Gmail settings → **See all settings** → **Forwarding and POP/IMAP**.
* Enable **IMAP Access**.
* Save changes.

#### Step 2: Create an App Password

* Visit: [https://myaccount.google.com/security](https://myaccount.google.com/security)
* Under **2-Step Verification**, click **App Passwords**.
* Select "Mail" and "Windows Computer" (or any name).
* Copy the 16-character password.

Use this in `.env` as your `EMAIL_PASSWORD`.

---

### ☁️ Google Drive API Setup

#### Step 1: Create a Google Cloud Project

* Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)
* Create a new project.

#### Step 2: Enable Google Drive API

* In your project dashboard, go to **APIs & Services** → **Library**.
* Search for **Google Drive API**, then enable it.

#### Step 3: Create OAuth Credentials

* Go to **APIs & Services** → **Credentials**.
* Click **Create Credentials** → **OAuth Client ID**.
* Choose **Desktop App**.
* Download the `credentials.json` file and place it in your project folder.

> The first time you run the script, a browser window will open for login and consent. A `token.json` file will be created for future runs.

---

### 📄 .env File Setup

Create a `.env` file in the root directory:

```ini
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_16_char_app_password
EMAIL_SENDER_FILTER=example@sender.com
EMAIL_SUBJECT_FILTER="Daily Transfer Report"
GDRIVE_FOLDER_ID=your_google_drive_folder_id
```

To get the `GDRIVE_FOLDER_ID`:

* Right-click the target folder in Google Drive → **Get link**.
* Copy the folder ID (the string after `/folders/` in the URL).

---

### 🚀 How to Run the Script

```bash
python gmail_to_drive.py
```

---

### 📌 Notes

* The script uses OAuth for Google Drive access. The `token.json` will be reused unless deleted.
* Files with the same name in the target Drive folder will **not be uploaded again**.
* Logs are printed to the terminal for success and error tracking.

---

### 🛠 Optional: Create `requirements.txt`

To regenerate your requirements file:

```bash
pip freeze > requirements.txt
```

---

### 🧼 Troubleshooting

* **Could not locate runnable browser**: Use `run_local_server()` instead of `run_console()`.
* **App password not working**: Ensure 2FA is enabled and you use the generated 16-char password.
* **Drive upload fails**: Double-check the `GDRIVE_FOLDER_ID` and MIME type handling.

---

### 📚 Credits

* Uses: `google-api-python-client`, `google-auth`, `imaplib2`, `dotenv`
* Inspired by real-world automation needs.

---