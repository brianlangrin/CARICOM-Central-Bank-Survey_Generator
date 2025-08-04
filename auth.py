from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from config import GMAIL_CREDENTIALS_PATH

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

FORM_ID=1a2b3c4d5e6f7g8h9i0jklmnopqrstuv
CSV_PATH=C:/Users/blang/CARICOM-FMI-Survey_Generator/recipients2.csv
GMAIL_CREDENTIALS_PATH=C:/Users/blang/CARICOM-FMI-Survey_Generator/client_secret_646864557402-kvjgts1aqs489e3a8nng2iqirh0ff0go.apps.googleusercontent.com.json
CREDENTIALS_FILE=C:/Users/blang/CARICOM-FMI-Survey_Generator/surveyautomation-465119-9f31891e08dc.json"
PROJECT_ID=surveyautomation-465119
TOKEN_PATH=C:/Users/blang/CARICOM-FMI-Survey_Generator/cbdc_token.pickle

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_credentials():
    creds = None
    if os.path.exists("cbdc_token.pickle"):
        with open("cbdc_token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(GMAIL_CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open("cbdc_token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return creds
