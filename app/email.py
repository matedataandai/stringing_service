from email.message import EmailMessage
import ssl
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()


class EmailSender:
    def __init__(self):
        self.sender_email = os.getenv("EMAIL_ADDRESS")
        self.sender_password = os.getenv("EMAIL_PASSWORD")

    def send_email(self, receiver_email, string, tension, unique_id,amount):
        msg = EmailMessage()
        msg["From"] = self.sender_email
        msg["To"] = receiver_email
        msg["Subject"] = "Thank you for your booking - Northern Beaches Tennis Stringing Services"
        body = f"""Thank you for your booking with Northern Beaches Tennis Stringing Services!

Your booking details:
- Amount: ${amount:.2f} AUD
- String: {string}
- Tension: {tension} lbs
- Unique stinging service: {unique_id}

Next step is to drop off your racket at Unit 1 3 Cameron Avenue, Manly.

Feel free to reach out to us at 0406292441 or reply to this email if you have any questions or need further assistance.

Best regards,
The Northern Beaches Stringing Services Team"""
        
        msg.set_content(body)

        context = ssl.create_default_context()

        try:
            print("Connecting to Gmail...")
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            print("Email sent successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")