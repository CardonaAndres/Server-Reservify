from fastapi import status
from datetime import timedelta
from fastapi.responses import JSONResponse
from src.schemas.schedule_schema import ScheduleSchema
from src.models.schedule_model import ScheduleModel
from src.utils.handle_exception import handle_exception
from src.utils.is_admin import is_user_admin

class ScheduleController:
    @staticmethod
    async def get_schedule_full():
        try:
            result = await ScheduleModel.get_schedule_full()
            
            if result is not None:
                for row in result:
                    
                    if isinstance(row.get("open_time"), timedelta):
                        row["open_time"] = str(row["open_time"])
                    if isinstance(row.get("close_time"), timedelta):
                        row["close_time"] = str(row["close_time"])
                        
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={'message': 'Todos los días del horario', 'data': result}
                )
                
            else:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={'message': 'No se encontraron horarios.', 'data': []}
                )

        except Exception as err:        
            return await handle_exception(err)
            
    @staticmethod
    async def get_schedule_day(id : int | str):
        try:
            result = await ScheduleModel.get_schedule_day(id)
            
            if result is not None:
                # Convertir timedelta a string en el controlador
                for key in ['open_time', 'close_time']:
                    if isinstance(result.get(key), timedelta):
                        result[key] = str(result[key])
                        
                return JSONResponse(
                    status_code = status.HTTP_200_OK,
                    content = result
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={ 'message': 'No se encontró un horario con el ID proporcionado.', 'data': {} }
                )
            
        except Exception as err:
            return await handle_exception(err)

    @staticmethod
    async def create_schedule_day(day : ScheduleSchema, user : dict):
        try:

            result = await is_user_admin(user['role_ID'])      
            if result: 
                return result    
            
            days = await ScheduleModel.get_schedule_full()
            
            for item in days:
                if item['weekday'] == day.weekday:
                    return JSONResponse( 
                        status_code = status.HTTP_400_BAD_REQUEST,
                        content = {
                            'message' : 'Dia ya registrado en la Base De Datos'
                        } 
                    )
            
            await ScheduleModel.register_day(day)
            
            return JSONResponse(
                status_code = status.HTTP_201_CREATED,
                content = {
                    'message' : 'Creado con exito'
                }  
            )
        
        except Exception as err:
            return await handle_exception(err)
      
    @staticmethod   
    async def update_schedule_day(day : ScheduleSchema, id : str | int, user : dict):
        try:
            result = await is_user_admin(user['role_ID'])      
            if result: 
                return result 
            
            await ScheduleModel.update_day(day, id)
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Día actualizado correctamente'
                }
            )
           
        except Exception as err:
            return await handle_exception(err)
            
    @staticmethod
    async def delete_day(id : str | int, user : dict):
        try:
            result = await is_user_admin(user['role_ID'])      
            if result: 
                return result
            
            day_to_delete = await ScheduleModel.get_schedule_day(id)
            
            if not day_to_delete:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'El día con el ID especificado no se encontró'
                    }
                )
            
            await ScheduleModel.delete_day(id) 
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Eliminado correctamente'
                }
            )
            
        except Exception as err:
           return await handle_exception(err)