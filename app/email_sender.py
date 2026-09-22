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
        msg["To"] = f'{receiver_email}, {self.sender_email}'
        msg["Subject"] = "Thank you for your booking - Northern Beaches Tennis Re-stringing Services"
        body = f"""Thank you for your booking with Northern Beaches Tennis Re-stringing Services!

Your booking details:
- Amount: ${amount:.2f} AUD
- String: {string}
- Tension: {tension} lbs
- Unique Stringing service: {unique_id}

Next step is to drop off your racket at Unit 1 3 Cameron Avenue, Manly.

Feel free to reach out to us at 0406292441 or reply to this email if you have any questions or need further assistance.

Best regards,
The Northern Beaches Re-stringing Services Team"""
        
        msg.set_content(body)

        try:
          print("Connecting to Gmail SMTP server...")
          with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
          print("Email sent successfully via Gmail!")
        except Exception as e:
          print(f"Error: {e}")