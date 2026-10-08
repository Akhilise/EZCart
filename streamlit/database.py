import os
from dotenv import load_dotenv
import mysql.connector as mysql
from mysql.connector import Error

# Load enviroment variables
load_dotenv()

# Get database credentials
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# Create SQL connection
try :
    connection = mysql.connect(
        host= DB_HOST,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )
    if connection.is_connected():
        print('Connected to MySQL database')
except Error as e:
    print('Error while connecting to MySQL', e)


finally:
    if connection.is_connected():
     connection.close()
     print('MySQL connection is closed')  
