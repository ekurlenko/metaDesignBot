from peewee import *
import peewee_async

from dataBase.config import db

class RoomTypeModel(peewee_async.AioModel):
    id = BigAutoField(primary_key=True)
    name = CharField(unique=True, max_length=100)

    class Meta:
        db_table = 'room_types'
        database = db
