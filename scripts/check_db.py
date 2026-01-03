import traceback
import mysql.connector
import os
from app.settings import DATABASE

def try_connect():
    masked_config = {
        "host": DATABASE.get("host"),
        "user": DATABASE.get("user"),
        "database": DATABASE.get("database"),
        "port": DATABASE.get("port"),
        "password_present": bool(DATABASE.get("password"))
    }
    print("Using DB config (password masked):", masked_config)

    try:
        conn = mysql.connector.connect(
            host=DATABASE.get("host"),
            user=DATABASE.get("user"),
            password=DATABASE.get("password"),
            database=DATABASE.get("database"),
            port=DATABASE.get("port", 3366),
            connection_timeout=5
        )
        print("Connected OK")
        conn.close()
    except Exception as e:
        print("Connection failed:", type(e), e)
        traceback.print_exc()

if __name__ == '__main__':
    try_connect()
