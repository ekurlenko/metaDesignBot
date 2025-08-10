from dataBase.models.RealtyStatusTypeModel import RealtyStatusTypeModel
from dataBase.repositories.base import BaseRepository


class RealtyStatusTypeRepository(BaseRepository):
    def find_by_name(self, name):
        result = RealtyStatusTypeModel.select().where(RealtyStatusTypeModel.name == name).first()
        return result
