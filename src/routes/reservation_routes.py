from fastapi import APIRouter, Depends, Query
from src.controllers.reservation_controller import ReservationController
from src.utils.verify_token import verify_token
from src.schemas.reservation_schema import ReservationSchema

reservation_router = APIRouter(prefix = '/reservations', tags=['Reservations'])

@reservation_router.get('/verify_reservations')
async def verify_reservations(user : dict = Depends(verify_token)):
    return await ReservationController.verify_reservations(user)

@reservation_router.get('/reservations')
async def get_all_reservations(user : dict = Depends(verify_token), page: int = Query(1, ge=1)):
    return await ReservationController.get_all_reservations(user, page)

@reservation_router.get('/all-reservations')
async def get_all_reservations_admin(user : dict = Depends(verify_token), page: int = Query(1, ge=1)):
    return await ReservationController.get_all_reservations_admin(user, page)

@reservation_router.get('/reservation/{id}')
async def get_reservation(id : int | str, user : dict = Depends(verify_token)):
    return await ReservationController.get_reservation(id, user)

@reservation_router.post('/reservation')
async def create_reservation(data : ReservationSchema, user : dict = Depends(verify_token)):
    return await ReservationController.create_reservation(data, user)

@reservation_router.put('/reservation/{id}')
async def update_reservation(id:int | str, data: ReservationSchema, user: dict = Depends(verify_token)):
    return await ReservationController.update_reservation(id, data, user)

@reservation_router.delete('/reservation/{id}')
async def delete_reservation(id: int | str, user: dict = Depends(verify_token)):
    return await ReservationController.delete_reservation(id, user)