from peewee import IntegrityError, ProgrammingError

from dataBase.models.PropertyTypeModel import  PropertyTypeModel
from dataBase.models.RepairClassModel import RepairClassModel
from dataBase.models.RoomTypeModel import RoomTypeModel

from misc.consts import NEW_BUILDING_EN, SECONDARY_EN, COMFORT_EN, BUSINESS_EN, FLAT_EN, HOUSE_EN, COMMERCIAL_EN, \
    PREMIUM_EN

try:
    RoomTypeModel.create(name=NEW_BUILDING_EN)
    RoomTypeModel.create(name=SECONDARY_EN)
    RepairClassModel.create(name=COMFORT_EN)
    RepairClassModel.create(name=BUSINESS_EN)
    RepairClassModel.create(name=PREMIUM_EN)
    PropertyTypeModel.create(name=FLAT_EN)
    PropertyTypeModel.create(name=HOUSE_EN)
    PropertyTypeModel.create(name=COMMERCIAL_EN)
except ProgrammingError:
    pass
except IntegrityError:
    pass