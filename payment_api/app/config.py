import os
from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://admin:admin@localhost:5432/payment_db")
