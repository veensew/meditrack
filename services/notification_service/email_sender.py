import smtplib
from email.message import EmailMessage
from config import Config

class EmailSender:
    @staticmethod
    async def send_email(to_email: str, subject: str, content: str) -> bool:
        msg = EmailMessage()
        msg["From"] = Config.SMTP_USERNAME
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.set_content(content)

        try:
            with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as s:
                s.starttls()
                s.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
                s.send_message(msg)
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False
