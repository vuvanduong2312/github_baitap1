import os
from dotenv import load_dotenv

# Load biến từ file .env (nếu có), nhưng ưu tiên environment từ Docker
load_dotenv()

class Config:
    # Secret key
    SECRET_KEY = os.getenv('SECRET_KEY', 'defaultsecret123')

    # Database URI - lấy từ docker-compose.yml
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    # Tắt warning không cần thiết
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask mode
    ENV = os.getenv('FLASK_ENV', 'production')