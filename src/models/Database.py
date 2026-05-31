import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class Database:
    @staticmethod
    def get_connection():
        try:
            connection = mysql.connector.connect(
                host = os.getenv('DB_HOST'),
                user = os.getenv('DB_USER'),
                password = os.getenv('DB_PASSWORD'),
                database = os.getenv('DB_NAME')
            )
            
            if connection.is_connected():
                return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")