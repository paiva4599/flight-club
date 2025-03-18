import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_SID")
account_key = os.getenv("TWILIO_KEY")
twilio_phone = os.getenv("TWILIO_PHONE")


class NotificationManager:
    def __init__(self):
        self.phone = f"whatsapp:{twilio_phone}"
        self.client = Client(account_sid, account_key)

    def send_message(self, phone, content):
        message = self.client.messages.create(
            from_= self.phone,
            body=content,
            to=phone
        )

        return message
