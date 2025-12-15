from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    title: str

class AppointmentOut(AppointmentCreate):
    id: int

    class Config:
        from_attributes = True
