from pydantic import BaseModel


class RealtyStatusTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
