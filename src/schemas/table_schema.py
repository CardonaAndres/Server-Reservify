from pydantic import BaseModel, Field, validator

class TableSchema(BaseModel):
    table_number: int = Field(..., ge=1, description="Número único de la mesa", example=1)
    capacity: int = Field(..., ge=1, description="Número de personas que puede acomodar", example=4)

    @validator('table_number')
    def check_table_number_non_negative(cls, v):
        if v < 1:
            raise ValueError("El número de la mesa debe ser un valor positivo mayor a cero.")
        return v

    @validator('capacity')
    def check_capacity_positive(cls, v):
        if v < 1:
            raise ValueError("La capacidad debe ser un número positivo mayor a cero.")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "table_number": 1,
                "capacity": 4,
            }
        }
