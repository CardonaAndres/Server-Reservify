from fastapi import APIRouter, Depends, Query
from src.utils.verify_token import verify_token
from src.controllers.payment_controller import PaymentController
from src.schemas.payment_schema import PaymentSchema

payment_router = APIRouter(prefix = '/payments', tags = ['Payments'])

@payment_router.get('/payments')
async def get_all_payments(user : dict = Depends(verify_token), page : int = Query(1, ge=1)):
    return await PaymentController.get_all_payments(user, page)

@payment_router.get('/payment/{id}')
async def get_payment(id : int | str, user : dict = Depends(verify_token)):
    return await PaymentController.get_payment(id, user)

@payment_router.post('/payment')
async def create_payment(data : PaymentSchema, user : dict = Depends(verify_token)):
    return await PaymentController.do_payment(data, user)
