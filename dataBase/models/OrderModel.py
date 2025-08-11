import datetime

from peewee import *

from dataBase.config import db
from dataBase.models.RealtyStatusTypeModel import RealtyStatusTypeModel
from dataBase.models.RealtyTypeModel import RealtyTypeModel
from dataBase.models.RepairTypeModel import RepairTypeModel
from dataBase.models.UserModel import UserModel


class OrderModel(Model):
    id = BigAutoField()
    user_id = ForeignKeyField(UserModel, backref="users")
    realty_type = ForeignKeyField(RealtyTypeModel, backref="realty_types")
    square = FloatField()
    realty_status_type = ForeignKeyField(RealtyStatusTypeModel, backref="realty_status_types")
    repair_type = ForeignKeyField(RepairTypeModel, backref="repair_types")
    cost = BigIntegerField()
    created_at = DateField(default=datetime.date.today())
    done_at = DateField(null=True)

    class Meta:
        db_table = 'orders'
        database = db
