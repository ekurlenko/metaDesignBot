from peewee import Model, BigAutoField, BigIntegerField, TextField, CharField

from dataBase.config import db


class UserModel(Model):
    id = BigAutoField()
    chat_id = BigIntegerField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    phone_number = CharField(unique=True, max_length=20)

    class Meta:
        db_table = 'users'
        database = db
