from pydantic import BaseModel


class RealtyTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
