from dataBase.models.RepairTypeModel import RepairTypeModel
from dataBase.repositories.base import BaseRepository


class RepairTypeRepository(BaseRepository):
    def find_by_name(self, name):
        result = RepairTypeModel.select().where(RepairTypeModel.name == name).first()
        return result
