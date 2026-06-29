import smtplib
from email.mime.text import MIMEText

from core.config import settings


def send_verification_code(to_email: str, code: str) -> None:
    subject = "Код подтверждения SoftLearn"
    body = f"Твой код подтверждения: {code}\nОн действует 10 минут."

    message = MIMEText(body, "plain", "utf-8")
    message["Subject"] = subject
    message["From"] = settings.smtp_from or settings.smtp_user
    message["To"] = to_email

    with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
        server.starttls()
        server.login(settings.smtp_user, settings.smtp_password)
        server.sendmail(message["From"], [to_email], message.as_string())
