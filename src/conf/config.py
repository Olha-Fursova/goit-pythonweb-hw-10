from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    DB_URL = os.getenv("DB_URL")

    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM", os.getenv("MAIL_USERNAME", ""))
    MAIL_SERVER: str = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT: int = int(os.getenv("MAIL_PORT", "465"))
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Contacts App")

    CLOUDINARY_NAME = os.getenv("CLOUDINARY_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")


settings = Settings()