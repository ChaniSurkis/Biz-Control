from fastapi import APIRouter
from app.schemas.appointment import AppointmentCreate, AppointmentOut
from app.services.appointment_service import create_appointment

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentOut)
def create(data: AppointmentCreate):
    return create_appointment(data)
