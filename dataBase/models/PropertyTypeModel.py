from peewee import *
import peewee_async

from dataBase.config import db


class PropertyTypeModel(peewee_async.AioModel):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'property_types'
        database = db
