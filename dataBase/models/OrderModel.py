import datetime

from dataBase.config import db
from dataBase.models.UserModel import UserModel
from dataBase.models.RoomTypeModel import RoomTypeModel
from dataBase.models.PropertyTypesModel import PropertyTypeModel
from dataBase.models.RepairClassesModel import RepairClassModel

from peewee import *
import peewee_async


class OrderModel(peewee_async.AioModel):
    id = BigAutoField()
    user_id = ForeignKeyField(UserModel, backref="orders")
    property_type = ForeignKeyField(PropertyTypeModel, backref="property_types")
    square = FloatField()
    room_type = ForeignKeyField(RoomTypeModel, backref="room_types")
    repair_class = ForeignKeyField(RepairClassModel, backref="repair_classes")
    cost = BigIntegerField()
    create_date = DateField(default=datetime.date.today())

    class Meta:
        db_table = 'orders'
        database = db


OrderModel.create_table(True)
