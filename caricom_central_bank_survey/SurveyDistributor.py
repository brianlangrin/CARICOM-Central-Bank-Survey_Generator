import base64
import csv
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from config import CSV_PATH

class SurveyDistributor:
    """Handles survey distribution and Gmail-based alert delivery."""

    def __init__(self, form_id: str, creds, template_mgr, csv_path: str = None):
        self.form_id = form_id
        self.creds = creds
        self.csv_path = csv_path or CSV_PATH
        self.form_url = f"https://docs.google.com/forms/d/{form_id}"
        self.recipients = self._load_recipients()
        self.gmail = build("gmail", "v1", credentials=creds)
        self.template_mgr = template_mgr

    def _load_recipients(self) -> list:
        recipients = []
        with open(self.csv_path, encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                recipients.append({
                    "institution": row["institution"].strip(),
                    "contact_name": row["contact_name"].strip(),
                    "emails": [email.strip() for email in row["emails"].split(",") if email.strip()]
                })
        return recipients

    def send_email(self, to: str, subject: str, body: str) -> None:
        print(f"DEBUG: to={to}, subject={subject}, body={body[:100]}")
        message = MIMEText(body, "html")
        message["to"] = to
        message["from"] = "me"
        message["subject"] = subject
    
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
        try:
            self.gmail.users().messages().send(userId="me", body={"raw": raw}).execute()
            print(f"✅ Sent email to {to}")
        except Exception as e:
            import traceback
            print(f"❌ Failed to send email to {to}: {e}")
            traceback.print_exc()


    def distribute_survey(self):
        print("Distributing survey to recipients:\n")
        for entry in self.recipients:
            print(f"{entry['institution']}: {', '.join(entry['emails'])}")
            for email in entry["emails"]:
                body = self.template_mgr.render(
                    "survey_invite",
                    name=entry["institution"],
                    survey_title="CARICOM Regional FMI Survey",
                    form_url=self.form_url
                )
                self.send_email(to=email, subject="CARICOM Survey Invitation", body=body)
        print(f"\n✅ Survey link: {self.form_url}")

