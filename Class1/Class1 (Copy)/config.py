import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

class Config:
    # Secret key
    SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")

    # Database URI (MySQL Docker)
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Tắt warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask mode
    ENV = os.getenv("FLASK_ENV", "production")
