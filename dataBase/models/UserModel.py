from dataBase.config import db

from peewee import *
import peewee_async


class UserModel(peewee_async.AioModel):
    id = BigAutoField()
    chat_id = BigIntegerField(null=True, unique=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    phone_number = TextField()

    class Meta:
        db_table = 'users'
        database = db


UserModel.create_table(True)
