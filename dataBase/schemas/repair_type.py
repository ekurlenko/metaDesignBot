from pydantic import BaseModel


class RepairTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
