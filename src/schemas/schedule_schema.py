from pydantic import BaseModel, Field, validator
from datetime import time
import unidecode

class ScheduleSchema(BaseModel):
    weekday: str = Field(..., description="Día de la semana", example="Lunes")
    open_time: time = Field(..., description="Hora de apertura", example="09:00:00")
    close_time: time = Field(..., description="Hora de cierre", example="17:00:00")

    @validator('weekday')
    def validate_weekday(cls, value):
        user_day = unidecode.unidecode(value).lower()
        days = [
            'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo',
            'lunes festivo', 'martes festivo', 'jueves festivo', 'viernes festivo'
        ]
        
        if user_day not in days:
            raise ValueError(f"El día debe ser uno de los siguientes: {', '.join(days)}")
        
        return value
    
    @validator('open_time', 'close_time')
    def validate_time_format(cls, value):
        
        if not isinstance(value, time):
            raise ValueError('Debe ser un valor de tipo time')
        return value
    
    @validator('close_time')
    def validate_close_time(cls, value, values):
        open_time = values.get('open_time')
        
        if open_time and value <= open_time:
            raise ValueError("La hora de cierre debe ser posterior a la hora de apertura.")
        return value

    class Config:
        #formato ISO para representar el time como HH:MM:SS
        json_encoders = {
            time: lambda v: v.strftime('%H:%M')
        }