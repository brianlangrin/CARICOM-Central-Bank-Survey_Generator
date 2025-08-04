# === Config ===
python-dotenv
os
google-auth
google-api-python-client

load_dotenv()

FORM_ID = os.getenv("FORM_ID")
CSV_PATH = os.getenv("CSV_PATH")
GMAIL_CREDENTIALS_PATH = os.getenv("GMAIL_CREDENTIALS_PATH")


PROJECT_ID = "surveyautomation-465119"
CREDENTIALS_FILE = r"C:\Users\blang\OneDrive\Google Forms Generator Code\surveyautomation-465119-9f31891e08dc.json"

# === Authenticate ===
credentials = service_account.Credentials.from_service_account_file(
    CREDENTIALS_FILE,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
crm_service = build("cloudresourcemanager", "v1", credentials=credentials)

# === Check IAM Permissions ===config.py
permissions_to_check = ["resourcemanager.projects.setIamPolicy"]

request_body = {
    "permissions": permissions_to_check
}

response = crm_service.projects().testIamPermissions(
    resource=PROJECT_ID,
    body=request_body
).execute()

granted = response.get("permissions", [])

if "resourcemanager.projects.setIamPolicy" in granted:
    print("✅ Service account HAS permission to set IAM policy.")
else:
    print("❌ Service account is MISSING permission to set IAM policy.")
