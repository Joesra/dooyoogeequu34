import os
from dotenv import load_dotenv

# .env staat in de bovenliggende map van 'app/'
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

DATABASE = {
    'NAME': os.getenv("DB_NAME"),
    'USER': os.getenv("DB_USER"),
    'PASSWORD': os.getenv("DB_PASSWORD"),
    'HOST': os.getenv("DB_HOST"),
    'PORT': int(os.getenv("DB_PORT")) if os.getenv("DB_PORT") else None
}