from peewee import *
import peewee_async

from dataBase.config import db

from misc.consts import COMMERCIAL, FLAT, HOUSE


class PropertyTypeModel(peewee_async.AioModel):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'property_types'
        database = db


# PropertyTypeModel.create_table(True)
# PropertyTypeModel.create(name=FLAT)
# PropertyTypeModel.create(name=HOUSE)
# PropertyTypeModel.create(name=COMMERCIAL)
