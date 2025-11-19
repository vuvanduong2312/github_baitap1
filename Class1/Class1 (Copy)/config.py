import os
from dotenv import load_dotenv

# Load biến từ file .env (local), nhưng khi chạy Docker thì environment của container sẽ override
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")

    # Database URI lấy từ Docker hoặc từ .env
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask mode
    ENV = os.getenv("FLASK_ENV", "production")
