from pydantic import BaseModel

class FoodTruckOut(BaseModel):
    id: int
    applicant: str
    status: str
    address: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True