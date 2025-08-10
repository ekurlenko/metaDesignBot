from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from dataBase.schemas.realty_status_type import RealtyStatusTypeSchema
from dataBase.schemas.realty_type import RealtyTypeSchema
from dataBase.schemas.repair_type import RepairTypeSchema
from dataBase.schemas.user import UserSchema


class OrderCreateSchema(BaseModel):
    user_id: UserSchema
    realty_type: RealtyTypeSchema
    square: float
    realty_status_type: RealtyStatusTypeSchema
    repair_type: RepairTypeSchema
    cost: int
    done_at: Optional[datetime] = datetime.now()
