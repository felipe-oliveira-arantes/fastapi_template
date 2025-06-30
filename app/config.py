import os

class Settings:
    # IMPORTANT: Replace 'db' with 'localhost' if your PostgreSQL is running directly on your machine.
    # Also, replace 'user' and 'password' with your actual PostgreSQL username and password.
    DATABASE_URL = "postgresql://clinic:123456@localhost:5432/clinic_db"

settings = Settings() 