from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.conf.config import settings
 
mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)
 
fm = FastMail(mail_config)
 
 
async def send_reset_password_email(email: str, token: str) -> None:
    reset_url = f"http://localhost:8000/api/auth/reset-password-confirm/{token}"
 
    body = f"""
    <h3>Password Reset Request</h3>
    <p>You requested a password reset. Click the link below:</p>
    <p><a href="{reset_url}">{reset_url}</a></p>
    <p>This link expires in <strong>15 minutes</strong>.</p>
    <p>If you did not request this, please ignore the email.</p>
    """
 
    message = MessageSchema(
        subject="Password Reset — Contacts App",
        recipients=[email],
        body=body,
        subtype=MessageType.html,
    )
 
    await fm.send_message(message)
 
 
async def send_verification_email(email: str, token: str) -> None:
    verify_url = f"http://localhost:8000/api/auth/verify/{token}"
 
    body = f"""
    <h3>Confirm your email</h3>
    <p>Click the link below to verify your account:</p>
    <p><a href="{verify_url}">{verify_url}</a></p>
    <p>If you did not register, please ignore this email.</p>
    """
 
    message = MessageSchema(
        subject="Email Verification — Contacts App",
        recipients=[email],
        body=body,
        subtype=MessageType.html,
    )
 
    await fm.send_message(message)