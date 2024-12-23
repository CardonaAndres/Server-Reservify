from pydantic import BaseModel, Field, EmailStr, validator
import re

class LoginSchema(BaseModel):
    email : EmailStr = Field(..., title="Correo Electrónico", example="usuario@example.com")
    password : str = Field(..., min_length = 8, title="Contraseña", example = "Password123")
    
class RegisterSchema(BaseModel):
    name : str = Field(..., min_length=2, max_length=100, title="Nombre", example="Juan Pérez")
    email : EmailStr = Field(...,  title="Correo Electrónico", example="usuario@example.com")
    cellphone : str = Field(..., max_length=20, pattern=r"^\+?\d{7,20}$", title="Número de Teléfono")
    password : str = Field(...,min_length=8, max_length=255)
    role_ID : int = Field(default=2, ge=1, le=5, title="Rol del Usuario")
    
    @validator("password")
    def validate_password(cls, value):
        # Validar al menos una letra mayúscula
        if not re.search(r'[A-Z]', value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        
        # Validar al menos una letra minúscula
        if not re.search(r'[a-z]', value):
            raise ValueError("La contraseña debe contener al menos una letra minúscula.")
        
        # Validar al menos un número
        if not re.search(r'[0-9]', value):
            raise ValueError("La contraseña debe contener al menos un número.")
        
        # Validar al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("La contraseña debe contener al menos un carácter especial (!@#$%^&*).")
        
        return value
    
class UpdatePasswordSchema(BaseModel):
    email : EmailStr = Field(..., title="Correo Electrónico", example="usuario@example.com")
    new_password : str = Field(..., min_length=8, title="Nueva Contraseña", max_length = 255)
    
    @validator("new_password")
    def validate_password(cls, value):
        # Validar al menos una letra mayúscula
        if not re.search(r'[A-Z]', value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        
        # Validar al menos una letra minúscula
        if not re.search(r'[a-z]', value):
            raise ValueError("La contraseña debe contener al menos una letra minúscula.")
        
        # Validar al menos un número
        if not re.search(r'[0-9]', value):
            raise ValueError("La contraseña debe contener al menos un número.")
        
        # Validar al menos un carácter especial
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("La contraseña debe contener al menos un carácter especial (!@#$%^&*).")
        
        return value