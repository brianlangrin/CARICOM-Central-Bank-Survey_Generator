class ReminderSystem:
    def setup_schedule(self, recipients, delay_days=3):
        """
        Simulate scheduling email reminders after a delay.
        """
        for r in recipients:
            for email in r["emails"]:
                print(f"Scheduled reminder to {email} in {delay_days} days (simulated)")
