from peewee import *
import peewee_async

from dataBase.config import db

from misc.consts import COMFORT, BUSINESS


class RepairClassModel(peewee_async.AioModel):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'repair_classes'
        database = db


# RepairClassModel.create_table(True)
# RepairClassModel.create(name=COMFORT)
# RepairClassModel.create(name=BUSINESS)
