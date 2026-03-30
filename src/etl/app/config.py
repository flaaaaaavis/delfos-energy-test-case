import os

API_URL = os.getenv("API_URL", "http://api:8000")
DB_TARGET = os.getenv("DB_TARGET", "postgresql://user:pass@target_db:5432/db")