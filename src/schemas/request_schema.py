from pydantic import BaseModel, Field
from typing import Optional

class ServiceRequestSchema(BaseModel):
    title: str = Field(..., min_length = 5, title="Título de la solicitud de servicio")
    description: str = Field(..., min_length = 5, title="Descripción de la solicitud de servicio")
    user_ID: Optional[int] = Field(title="ID del usuario", default = 0)