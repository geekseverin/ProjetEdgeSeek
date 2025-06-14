from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config import settings  # ou depuis ton module de settings
from typing import List
from pydantic import EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM == 587,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS == True,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS == False,
    USE_CREDENTIALS = True,
    MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
    VALIDATE_CERTS = True,
)

async def send_email(subject: str, recipients: List[EmailStr], body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,  # List of recipients
        body=body,
        subtype="html"  # or "plain"
    )
    fm = FastMail(conf)
    await fm.send_message(message)



conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = settings.MAIL_STARTTLS,
    MAIL_SSL_TLS = settings.MAIL_SSL_TLS,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True,
)
