# Define the class first
class RecipientsManager:
    """
    Handles loading and structuring recipient data for survey invites/reminders.
    """
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.recipients = self._load_recipients(self.csv_path)


    def _load_recipients(self, file_path: str) -> list:
        recipients = []
        with open(self.csv_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                recipients.append({
                    "institution": row["institution"],
                    "contact_name": row["contact_name"],
                    "emails": [e.strip() for e in row["emails"].split(",") if e.strip()]
                })
        return recipients

    def get_all(self):
        return self.recipients

    def get_by_institution(self, name):
        return [r for r in self.recipients if r["institution"].lower() == name.lower()]

    def get_all_emails(self):
        return [email for r in self.recipients for email in r["emails"]]

# Now instantiate after the class is defined
manager = RecipientsManager(csv_path=CSV_PATH)

