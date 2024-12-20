import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "kavinsewmina2000@gmail.com")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "gczu elrl zkbt hwlr")
    MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://kavinsewmina2000:Kibc9dQFmk56H1ho@cluster0.rsh2r.mongodb.net")
    DB_NAME = os.getenv("DB_NAME", "meditrack")