from peewee import IntegrityError, ProgrammingError

from dataBase.models.RealtyTypeModel import  RealtyTypeModel
from dataBase.models.RepairTypeModel import RepairTypeModel
from dataBase.models.RealtyStatusTypeModel import RealtyStatusTypeModel

from misc.consts import NEW_BUILDING_EN, SECONDARY_EN, COMFORT_EN, BUSINESS_EN, FLAT_EN, HOUSE_EN, COMMERCIAL_EN, \
    PREMIUM_EN

try:
    RealtyStatusTypeModel.create(name=NEW_BUILDING_EN)
    RealtyStatusTypeModel.create(name=SECONDARY_EN)
    RepairTypeModel.create(name=COMFORT_EN)
    RepairTypeModel.create(name=BUSINESS_EN)
    RepairTypeModel.create(name=PREMIUM_EN)
    RealtyTypeModel.create(name=FLAT_EN)
    RealtyTypeModel.create(name=HOUSE_EN)
    RealtyTypeModel.create(name=COMMERCIAL_EN)
except ProgrammingError:
    pass
except IntegrityError:
    pass