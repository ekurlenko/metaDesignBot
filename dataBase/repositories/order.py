from datetime import datetime

from dataBase.models.OrderModel import OrderModel
from dataBase.repositories.base import BaseRepository


class OrderRepository(BaseRepository):
    def create(self, data: dict) -> OrderModel:
        with self.db.atomic():
            order = OrderModel.create(
                **data,
                done_at=datetime.now()
            )
            return order