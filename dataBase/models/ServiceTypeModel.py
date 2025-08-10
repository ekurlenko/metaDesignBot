from peewee import *

from dataBase.config import db


class ServiceTypeModel(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'service_type'
        database = db
