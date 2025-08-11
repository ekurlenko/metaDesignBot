import os
from peewee import MySQLDatabase
from dotenv import load_dotenv

load_dotenv()

db = MySQLDatabase(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    host=os.getenv('DB_HOST'),
    password=os.getenv('DB_PASSWORD', default='')
)
