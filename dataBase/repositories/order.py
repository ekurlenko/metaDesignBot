from datetime import datetime
from typing import List

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

    def get_not_done(self) -> List[OrderModel]:
        result = OrderModel.select().where(OrderModel.done_at == None)
        return result

    def update_done_at(self, order: OrderModel) -> None:
        order.done_at = datetime.now()
        order.save()
