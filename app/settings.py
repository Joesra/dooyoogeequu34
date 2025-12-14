import os
from dotenv import load_dotenv

#.env staat in de bovenliggende map van 'app/'
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

DATABASE = {
    'NAME': os.getenv("DATABASE_NAME"),
    'USER': 'pb3bims2526_dooyoogeequu34',
    'PASSWORD': os.getenv("DB_PASSWORD"),
    'HOST': 'db.hbo-ict.cloud',
    'PORT': 3366
}