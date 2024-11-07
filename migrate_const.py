from peewee import IntegrityError, ProgrammingError

from dataBase.models.PropertyTypeModel import  PropertyTypeModel
from dataBase.models.RepairClassModel import RepairClassModel
from dataBase.models.RoomTypeModel import RoomTypeModel

from misc.consts import NEW_BUILDING, SECONDARY, COMFORT, BUSINESS, FLAT, HOUSE, COMMERCIAL

try:
    RoomTypeModel.create(name=NEW_BUILDING)
    RoomTypeModel.create(name=SECONDARY)
    RepairClassModel.create(name=COMFORT)
    RepairClassModel.create(name=BUSINESS)
    PropertyTypeModel.create(name=FLAT)
    PropertyTypeModel.create(name=HOUSE)
    PropertyTypeModel.create(name=COMMERCIAL)
except ProgrammingError:
    pass
except IntegrityError:
    pass