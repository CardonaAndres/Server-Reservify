from pydantic import BaseModel, Field
from decimal import Decimal

class PaymentSchema(BaseModel):
    reservation_ID : int = Field(..., title="ID de reserva")
    amount: Decimal = Field( title="Monto", ge=0, default = Decimal("80.500") ) 
    payment_method: str = Field(..., max_length=50, title="Método de pago")
    status: str = Field(max_length=50, title="Estado", default = "En proceso")
    
        # Personalizar el formato de Decimal en JSON
    class Config:
        json_encoders = {
            Decimal: lambda v: f"{v:.3f}"  
        }