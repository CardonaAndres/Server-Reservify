from fastapi import APIRouter, Depends
from src.controllers.schedule_controller import ScheduleController
from src.schemas.schedule_schema import ScheduleSchema
from src.utils.verify_token import verify_token

schedule_router = APIRouter(prefix='/schedules', tags=['Schedules'])

@schedule_router.get('/schedules')
async def schedule_full():
    return await ScheduleController.get_schedule_full()

@schedule_router.get('/schedule/{id}')
async def schedule_day(id : str | int):
    return await ScheduleController.get_schedule_day(id)

@schedule_router.post('/schedule')
async def create_schedule(day : ScheduleSchema, user : dict = Depends(verify_token)):
    return await ScheduleController.create_schedule_day(day, user)

@schedule_router.put('/schedule/{id}')
async def update_schedule(day : ScheduleSchema, id : str | int, user : dict = Depends(verify_token)):
    return await ScheduleController.update_schedule_day(day, id, user)

@schedule_router.delete('/schedule/{id}')
async def delete_schedule(id : str | int, user : dict = Depends(verify_token)):
    return await ScheduleController.delete_day(id, user)


