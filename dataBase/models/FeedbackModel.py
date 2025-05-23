import datetime

import peewee_async
from peewee import *

from dataBase.config import db
from dataBase.models.UserModel import UserModel
from dataBase.models.ServiceTypeModel import ServiceTypeModel


class FeedbackModel(peewee_async.AioModel):
    id = BigAutoField()
    user_id = ForeignKeyField(UserModel, backref='users')
    service_type = ForeignKeyField(ServiceTypeModel, backref='service_type')
    phone_call = BooleanField(default=False)
    telegram = BooleanField(default=False)
    whatsapp = BooleanField(default=False)
    created_at = DateField(default=datetime.date.today())
    done_at = DateField(null=True)

    class Meta:
        database = db
        table_name = 'feedback'
