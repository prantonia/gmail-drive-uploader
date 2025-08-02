import imaplib
import email
import os
import io
import logging
from dotenv import load_dotenv
from email.header import decode_header
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from mimetypes import guess_type

# ====== CONFIGURATION ======
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
SENDER_FILTER = os.getenv("SENDER_FILTER")
GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID")

SCOPES = ['https://www.googleapis.com/auth/drive.file']

# ====== LOGGING SETUP ======
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attachment_uploader.log'),
        logging.StreamHandler()
    ]
)

# Suppress noisy discovery_cache warning
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)

# ====== GOOGLE AUTH ======
def authenticate_google_drive():
    """
    Authenticate with Google Drive using refreshable OAuth2 credentials 
    (suitable for non-interactive environments like GitHub Actions).
    """
    try:
        creds = Credentials.from_authorized_user_info({
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "refresh_token": os.environ["GOOGLE_REFRESH_TOKEN"],
            "token_uri": "https://oauth2.googleapis.com/token"
        })

        if not creds.valid:
            creds.refresh(Request())

        logging.info("Authenticated with Google Drive.")
        return build('drive', 'v3', credentials=creds)

    except Exception as e:
        logging.error("Google Drive authentication failed: %s", e)
        raise

# ====== UPLOAD FUNCTION ======

def upload_to_drive(service, file_name, file_stream, mime_type):
    """
    Upload a file stream to a specific folder in Google Drive, skipping if the file name already exists.

    Parameters:
        service: Google Drive API client
        file_name: Name to use in Drive
        file_stream: io.BytesIO object
        mime_type: Detected MIME type of the file
    """
    try:
        # Check if a file with the same name already exists in the folder
        query = f"name = '{file_name}' and '{GDRIVE_FOLDER_ID}' in parents and trashed = false"
        response = service.files().list(q=query, spaces='drive', fields='files(id, name)').execute()
        existing_files = response.get('files', [])

        if existing_files:
            logging.info(f"Skipped upload: '{file_name}' already exists in Google Drive.")
            return

        # Proceed to upload if no duplicate
        file_metadata = {'name': file_name, 'parents': [GDRIVE_FOLDER_ID]}
        media = MediaIoBaseUpload(file_stream, mimetype=mime_type)
        result = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        logging.info(f"Uploaded '{file_name}' to Google Drive (File ID: {result['id']})")

    except Exception as e:
        logging.error(f"Failed to upload '{file_name}' to Drive: {e}")



# ====== DOWNLOAD & UPLOAD ======
def download_email_attachments():
    """
    Connects to Gmail via IMAP, filters unread emails from a sender,
    and uploads any .csv or .xlsx attachments to Google Drive.
    """
    try:
        if not all([EMAIL_USER, EMAIL_PASS, SENDER_FILTER, GDRIVE_FOLDER_ID]):
            logging.error("One or more environment variables are missing. Check .env file.")
            return

        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select('inbox')

        status, messages = mail.search(None, f'(UNSEEN FROM "{SENDER_FILTER}")')
        if status != 'OK':
            logging.warning("Failed to search inbox.")
            return

        msg_ids = messages[0].split()
        if not msg_ids:
            logging.info(f"No new emails from {SENDER_FILTER}.")
            return

        service = authenticate_google_drive()

        for msg_id in msg_ids:
            try:
                status, msg_data = mail.fetch(msg_id, '(RFC822)')
                if status != 'OK':
                    logging.warning(f"Failed to fetch message ID {msg_id.decode()}.")
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                        continue

                    filename = part.get_filename()
                    if filename and filename.lower().endswith(('.csv', '.xlsx')):
                        file_data = part.get_payload(decode=True)
                        file_stream = io.BytesIO(file_data)
                        mime_type = part.get_content_type()

                        upload_to_drive(service, filename, file_stream, mime_type)
            except Exception as e:
                logging.error(f"Error processing email ID {msg_id.decode()}: {e}")

        mail.logout()
        logging.info("Processing complete. Disconnected from email.")
    except imaplib.IMAP4.error as e:
        logging.error("IMAP error: %s", e)
    except Exception as e:
        logging.error("General error: %s", e)

# ========== ENTRY POINT ==========
if __name__ == '__main__':
    download_email_attachments()
