from pydantic import BaseModel, validator, Field
from datetime import date, time
from typing import Optional

class ReservationSchema(BaseModel):
    reservation_date : date = Field(..., title="Fecha de la Reserva")
    reservation_time: time = Field(..., title="Hora de la Reserva")
    status : Optional[str] = Field(title="Estado de la Reserva", default = "pendiente")
    user_ID : Optional[int] = Field(title="ID del Usuario", default=0)
    table_ID : int = Field(..., title="ID de la Mesa")
    
    @validator("reservation_date")
    def validate_reservation_date(cls, value):
        if value < date.today():
            raise ValueError("La fecha de la reserva no puede ser anterior a la fecha actual.")
           
        return value
    
    @validator("status")
    def validate_status(cls, value):
        allowed_statuses = ["confirmada", "cancelada", "pendiente", "finalizada"]
        if value.lower() not in allowed_statuses:
            raise ValueError(f"El estado debe ser uno de los siguientes: {', '.join(allowed_statuses)}.")
        return value.lower()
    
    class Config:
        #formato ISO para representar el time como HH:MM:SS
        json_encoders = {
            time: lambda v: v.strftime('%H:%M')
        }
        
        json_schema_extra = {
            "example": {
                "reservation_date": "2024-12-10",
                "reservation_time": "19:30",
                "status": "Pendiente",
                "user_ID": 0,
                "table_ID": 0
            }
        }