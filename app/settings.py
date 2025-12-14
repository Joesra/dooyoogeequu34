import os
from dotenv import load_dotenv

# .env staat in de bovenliggende map van 'app/'
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

DATABASE = {
    "host": "db.hbo-ict.cloud",
    "user": "pb3bims2526_dooyoogeequu34",
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DATABASE_NAME"),
    "port": int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else 3366
}
