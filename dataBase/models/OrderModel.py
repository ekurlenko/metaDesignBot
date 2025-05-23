import datetime

from dataBase.config import db
from dataBase.models.UserModel import UserModel
from dataBase.models.RoomTypeModel import RoomTypeModel
from dataBase.models.PropertyTypeModel import PropertyTypeModel
from dataBase.models.RepairClassModel import RepairClassModel

from peewee import *
import peewee_async


class OrderModel(peewee_async.AioModel):
    id = BigAutoField()
    user_id = ForeignKeyField(UserModel, backref="users")
    property_type = ForeignKeyField(PropertyTypeModel, backref="property_types")
    square = FloatField()
    room_type = ForeignKeyField(RoomTypeModel, backref="room_types")
    repair_class = ForeignKeyField(RepairClassModel, backref="repair_classes")
    cost = BigIntegerField()
    created_at = DateField(default=datetime.date.today())
    done_at = DateField(null=True)

    class Meta:
        db_table = 'orders'
        database = db

