import datetime

from peewee import *

from dataBase.config import db
from dataBase.models.ServiceTypeModel import ServiceTypeModel
from dataBase.models.UserModel import UserModel


class FeedbackModel(Model):
    id = BigAutoField()
    user_id = ForeignKeyField(UserModel, backref='users')
    service_type = ForeignKeyField(ServiceTypeModel, backref='service_type')
    phone_call = BooleanField(default=False)
    telegram = BooleanField(default=False)
    whatsapp = BooleanField(default=False)
    created_at = DateField(default=datetime.date.today())
    done_at = DateField(null=True)

    class Meta:
        table_name = 'feedback'
        database = db
