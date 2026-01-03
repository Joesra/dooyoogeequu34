import os
from dotenv import load_dotenv

# .env staat in de project-root (naast app/)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)

DATABASE = {
    "host": os.getenv("DB_HOST", "db.hbo-ict.cloud"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT", 3366)),
}
