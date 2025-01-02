from pydantic import BaseModel, Field, EmailStr

class ChangeRoleSchema(BaseModel):
    email : EmailStr = Field(..., title="Correo Electrónico", example="usuario@example.com")
    role_ID : int = Field(..., title="Nuevo Rol del Usuario")
    
class UpdateUserSchema(BaseModel):
    name : str = Field(..., min_length=2, max_length=100, title="Nombre", example="Juan Pérez")
    email : EmailStr = Field(...,  title="Correo Electrónico", example="usuario@example.com")
    cellphone : str = Field(..., max_length=20, pattern=r"^\+?\d{7,20}$", title="Número de Teléfono")