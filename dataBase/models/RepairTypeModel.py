from peewee import *

from dataBase.config import db


class RepairTypeModel(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'repair_types'
        database = db
