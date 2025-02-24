from peewee import *
import peewee_async

from dataBase.config import db

class RepairClassModel(peewee_async.AioModel):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'repair_classes'
        database = db
