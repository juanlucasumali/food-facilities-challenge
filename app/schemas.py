from pydantic import BaseModel, ConfigDict

class FoodTruckOut(BaseModel):
    id: int
    applicant: str
    status: str
    address: str
    latitude: float
    longitude: float

    model_config = ConfigDict(from_attributes=True)