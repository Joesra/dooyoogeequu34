import mysql.connector
from app.settings import DATABASE

def get_db_connection():
    return mysql.connector.connect(
        host=DATABASE["host"],
        user=DATABASE["user"],
        password=DATABASE["password"],
        database=DATABASE["database"],
        port=DATABASE["port"],
    )