# auto-generated snapshot
from peewee import *
import datetime
import peewee


snapshot = Snapshot()


@snapshot.append
class UserModel(peewee.Model):
    id = BigAutoField(primary_key=True)
    chat_id = BigIntegerField(null=True)
    first_name = TextField(null=True)
    last_name = TextField(null=True)
    phone_number = CharField(max_length=20, unique=True)
    class Meta:
        table_name = "users"


@snapshot.append
class PropertyTypeModel(peewee.Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    class Meta:
        table_name = "property_types"


@snapshot.append
class RoomTypeModel(peewee.Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    class Meta:
        table_name = "room_types"


@snapshot.append
class RepairClassModel(peewee.Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=100, unique=True)
    class Meta:
        table_name = "repair_classes"


@snapshot.append
class OrderModel(peewee.Model):
    id = BigAutoField(primary_key=True)
    user_id = snapshot.ForeignKeyField(backref='orders', index=True, model='usermodel')
    property_type = snapshot.ForeignKeyField(backref='property_types', index=True, model='propertytypemodel')
    square = FloatField()
    room_type = snapshot.ForeignKeyField(backref='room_types', index=True, model='roomtypemodel')
    repair_class = snapshot.ForeignKeyField(backref='repair_classes', index=True, model='repairclassmodel')
    cost = BigIntegerField()
    created_at = DateField(default=datetime.date(2024, 11, 7))
    done_at = DateField()
    class Meta:
        table_name = "orders"


def migrate_forward(op, old_orm, new_orm):
    op.run_data_migration()
    op.drop_column(old_orm.ordermodel.a)


def backward(old_orm, new_orm):
    ordermodel = new_orm['ordermodel']
    return [
        # Apply default value 0 to the field ordermodel.a,
        ordermodel.update({ordermodel.a: 0}).where(ordermodel.a.is_null(True)),
    ]


def migrate_backward(op, old_orm, new_orm):
    op.add_column(new_orm.ordermodel.a)
    op.run_data_migration()
    op.add_not_null(new_orm.ordermodel.a)
