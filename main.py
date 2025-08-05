os
python-dotenv

from caricom_central_bank_survey import CentralBankGoogleFormsGenerator, RecipientsManager, EmailTemplateManager, SurveyDistributor, ReminderSystem
from auth import get_gmail_credentials

from config import FORM_ID, CSV_PATH



def main():
    import os
    from dotenv import load_dotenv
    load_dotenv()

    form_id = os.getenv("FORM_ID")#
    csv_path = os.getenv("CSV_PATH")

    print("🔐 Authenticating Gmail API...")
    creds = get_gmail_credentials()

    print("📨 Loading recipients...")
    recipients_mgr = RecipientsManager(csv_path)
    recipients = recipients_mgr.get_all()

    print("📨 Initializing Survey Distributor...")
    template_mgr = EmailTemplateManager()
    distributor = SurveyDistributor(form_id=form_id, creds=creds, template_mgr=template_mgr)
    distributor.recipients = recipients  # Inject recipients 

    print("🚀 Distributing survey...")
    distributor.distribute_survey()

if __name__ == "__main__":
    main()


import re
import sys

def safe_sanitize(raw):
    return re.sub(r"font-family[:;]?.*?;", "", raw or "", flags=re.IGNORECASE)

def load_recipients(path):
    try:
        rm = RecipientsManager(path)
        recipients = rm.get_all()
        if not recipients:
            raise ValueError("No recipients found.")
        return recipients
    except Exception as e:
        print(f"❌ Failed to load recipients: {e}")
        return []

def initialize_generator(csv_path, creds_path, token_path, recipients):
    try:
        print("🔍 Attempting to initialize CentralBankGoogleFormGenerator...")
        gen = CentralBankGoogleFormGenerator(csv_path, creds_path, token_path)
        print("✅ Generator initialized.")
        gen.recipients = recipients
        return gen
    except Exception as e:
        print(f"❌ Generator initialization failed: {e}")
        return None

def build_form(generator):
    try:
        form_id = generator.create_centralbank_survey()
        if not form_id:
            raise ValueError("Form creation failed.")
        return form_id, f"https://docs.google.com/forms/d/{form_id}/viewform"
    except Exception as e:
        print(f"❌ Form creation error: {e}")
        return None, None

def generate_summary(creds, form_url):
    try:
        doc_url = create_doc_summary(creds, form_url, "CARICOM Survey")
        if not doc_url:
            raise ValueError("Document generation failed.")
        return doc_url
    except Exception as e:
        print(f"❌ Doc summary error: {e}")
        return None

def dispatch_invitations(form_id, creds, csv_path):
    try:
        template_mgr = EmailTemplateManager()
        distributor = SurveyDistributor(form_id, creds, template_mgr, csv_path)
        distributor.distribute_survey()
    except Exception as e:
        logger.error(f"Survey distribution failed: {e}", exc_info=True)
        traceback.print_exc()
		
def run_distribution_pipeline(form_id, creds):
    """
    Instantiates the email template manager and survey distributor,
    then sends templated survey invitations via Gmail API.
    """
    from email_templates import EmailTemplateManager  # or wherever it lives

    template_mgr = EmailTemplateManager()

    distributor = SurveyDistributor(
        form_id=form_id,
        creds=creds,
        template_mgr=template_mgr
    )
    distributor.distribute_survey()


def schedule_reminders(recipients):
    try:
        reminder = ReminderSystem()
        reminder.setup_schedule(recipients)
    except Exception as e:
        print(f"❌ Reminder scheduling failed: {e}")

# === Main Entry Point ===
if __name__ == "__main__":
    try:
        csv_path    = CVS_PATH
        creds_path  = CREDENTIALS_PATH
        token_path  = TOKEN_PATH

        recipients = load_recipients(csv_path)
        if not recipients: sys.exit()

        generator = initialize_generator(csv_path, creds_path, token_path, recipients)
        if not generator: exit()

        form_id, form_url = build_form(generator)
        if not form_id or not form_url: exit()
        print(f"✅ Google Form created:\n  {form_url}")

        doc_url = generate_summary(generator.creds, form_url)
        if not doc_url: exit()
        print(f"📄 Summary document created:\n  {doc_url}")

        print("\n📨 Ready to distribute to:")
        for entry in recipients:
            print(f"  {entry['institution']}: {', '.join(entry['emails'])}")

        confirm = input("\n🗣  Type 'yes' to send invitations: ").strip().lower()
        if confirm == "yes":
            dispatch_invitations(form_id, generator.creds, csv_path)
        else:
            print("🚫 Email distribution canceled.")

        schedule_reminders(recipients)

    except Exception as e:
        print(f"\n❌ Error running survey pipeline: {e}")
