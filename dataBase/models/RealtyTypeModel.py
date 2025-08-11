from peewee import *

from dataBase.config import db


class RealtyTypeModel(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'realty_types'
        database = db
