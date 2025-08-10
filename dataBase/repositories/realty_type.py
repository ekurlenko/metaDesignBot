from dataBase.models.RealtyTypeModel import RealtyTypeModel
from dataBase.repositories.base import BaseRepository


class RealtyTypeRepository(BaseRepository):
    def find_by_name(self, name: str) -> RealtyTypeModel:
        result = RealtyTypeModel.select().where(RealtyTypeModel.name == name).first()
        return result
