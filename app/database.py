import mysql.connector
from app.settings import DATABASE

def get_connection():
    return mysql.connector.connect(**DATABASE)