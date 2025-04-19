import os
import pickle
# Gmail API utilities
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError


# Request all access (permission to read/send/receive emails, manage the inbox, and more)
#SCOPES = ['https://mail.google.com/']
# Read all resources and their metadata—no write operations.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate(log_file):
    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    creds = None

    # If token.pickle exists, load the file
    if os.path.exists(str(CURR_DIR)+"/token.pickle"):
        with open(str(CURR_DIR)+"/token.pickle", "rb") as token:
            creds = pickle.load(token)

    # If token.pickle does not exists, generate the pickle file using credentials 
    # (client secret taken from Gmail API dashboard)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            credential_file = str(CURR_DIR)+'/credentials.json'
            flow = InstalledAppFlow.from_client_secrets_file(credential_file, SCOPES)
            creds = flow.run_local_server(port = 0)
        # save the credentials for the next run
        with open(str(CURR_DIR)+"/token.pickle", "wb") as token:
            pickle.dump(creds, token)
        
    try:
        service = build('gmail', 'v1', credentials = creds)
        return service
    except HttpError as error:
        log_file.write(f"Gmail Authentication Error: \n")
        log_file.write(f"Response: {error.resp}")
        return None


# get the Gmail API service
#service = gmail_authenticate()

