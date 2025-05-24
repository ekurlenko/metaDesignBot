import os
import peewee_async
from dotenv import load_dotenv

load_dotenv()

db = peewee_async.PooledMySQLDatabase(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    host=os.getenv('DB_HOST'),
    pool_params={
        "minsize": 2,
        "maxsize": 10,
        "pool_recycle": 55
    },
    password=os.getenv('DB_PASSWORD', default='')
)


