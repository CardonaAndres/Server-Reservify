from fastapi import status
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from src.utils.reservation_helpers import format_dates, format_date, convert_timedelta_to_time
from src.models.reservation_model import ReservationModel
from src.models.table_model import TableModel
from src.utils.is_admin import is_user_admin
from src.models.user_model import UserModel
from src.schemas.reservation_schema import ReservationSchema
from src.utils.handle_exception import handle_exception

class ReservationController:
    @staticmethod
    async def get_all_reservations_admin(user : dict, page : int = 1):
        try:
            not_admin = await is_user_admin(user['role_ID'])
            if not_admin:
                return not_admin
            
            reservations = await ReservationModel.get_all_reservations_admin(page)
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'reservations': format_dates(reservations['reservations']),
                    'total_count': reservations['total_count'],
                    'total_pages': reservations['total_pages'],
                    'current_page': reservations['current_page']  
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def get_all_reservations(user : dict, page : int = 1):
        try:
            user_response = await UserModel.get_user_by_ID(user['user_ID'])
            if not user_response:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'Usuario no encontrado'
                    }
                )
            
            user_reservations = await ReservationModel.get_reservations_paginate(
                user['user_ID'], page
            )
                      
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Estas son tus reservas: ',
                    'reservations': format_dates(user_reservations['reservations']),
                    'total_count': user_reservations['total_count'],
                    'total_pages': user_reservations['total_pages'],
                    'current_page': user_reservations['current_page']  
                }
            )
          
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def get_reservation(id : int | str, user : dict):
        try:
            not_admin = await is_user_admin(user['role_ID'])
            if not_admin:
                return not_admin
            
            reservation = await ReservationModel.get_reservation(id)
            
            if not reservation:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'La reserva no ha sido encontrada'
                    }
                )
                        
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Reserva encontrada',
                    'reservation' : format_date(reservation)
                }
            )
             
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def create_reservation(data : ReservationSchema, user : dict):
        try:
            reservations = await ReservationModel.get_reservations()  
            existing_table = await TableModel.get_table(data.table_ID)
            
            if not existing_table:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'La mesa deseada no fue encontrada'
                    }
                ) 
                
            # Convierte fecha y hora de la nueva reserva facilitar comparaciones
            new_reservation_datetime = datetime.combine(data.reservation_date, data.reservation_time)
            buffer_time = timedelta(minutes=40)
    
            for item in reservations:
                
                # Convertir 'reservation_date' y 'reservation_time'
                existing_date = item['reservation_date']
                existing_time = convert_timedelta_to_time(item['reservation_time'])
                    
                # Combinar fecha y hora de la reserva existente
                existing_reservation_datetime = datetime.combine(existing_date, existing_time)
                
                # Verificar si es la misma mesa y si existe un conflicto de tiempo
                if item['table_ID'] == data.table_ID:
                    time_difference = abs(existing_reservation_datetime - new_reservation_datetime)
                    invalid_statuses = {"cancelada", "finalizada"}
                    
                    if (item['user_ID'] == user['user_ID'] and item['status'] not in 
                        invalid_statuses and time_difference < buffer_time):
                        
                        status_reserva = item['status']
                        
                        return JSONResponse(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            content = {
                                'message' : f"Esta mesa ya tiene una reserva {status_reserva}  a tu nombre, en la fecha y hora dada"
                            }
                        )
                    
                    
                    if (time_difference < buffer_time 
                        and item['status'].lower() == 'confirmado'):                 
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "message": "Conflicto de reservas: ya existe una reserva cercana para esta mesa, o tienes una reserva para esta mesa."
                            }
                        )
                        
            user_response = await UserModel.get_user_by_ID(user['user_ID'])
            if not user_response:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'Usuario no encontrado'
                    }
                )
            
            data.user_ID = user['user_ID']
            
            await ReservationModel.create_reservation(data)
                     
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content={
                    "message": "Reserva creada exitosamente."
                }
            )
                
                     
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def update_reservation(id : int | str, data : ReservationSchema, user : dict):
        try:
            is_not_admin = await is_user_admin(user['role_ID'])
            if is_not_admin:
                return is_not_admin
            
            existing_reservation = await ReservationModel.get_reservation(id)
            existing_table = await TableModel.get_table(data.table_ID)
            
            if(existing_reservation['status'].lower()) == 'confirmada':
                data.status = existing_reservation['status']

            if not existing_table:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'La mesa deseada no fue encontrada'
                    }
                ) 
            
            if not existing_reservation:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'Reserva no encontrada'
                    }
                )
                
            reservations = await ReservationModel.get_reservations() 
            
            # Convierte la nueva fecha y hora para facilitar comparaciones
            new_reservation_datetime = datetime.combine(data.reservation_date, data.reservation_time)
            buffer_time = timedelta(minutes=40)     
            
            for item in reservations:
                # Si la reserva es la misma (por tabla, fecha y hora), ignórala
                if (
                    item['reservation_date'] == existing_reservation['reservation_date'] and
                    item['reservation_time'] == existing_reservation['reservation_time'] and
                    item['table_ID'] == existing_reservation['table_ID']
                ):
                    continue 
                
                # Convertir fecha y hora de la reserva existente
                existing_date = item['reservation_date']
                existing_time = convert_timedelta_to_time(item['reservation_time'])                  
                existing_reservation_datetime = datetime.combine(existing_date, existing_time)
                      
                # Verificar conflicto de horarios en la misma mesa
                if item['table_ID'] == data.table_ID:
                    
                    time_difference = abs(existing_reservation_datetime - new_reservation_datetime)
                    
                    if time_difference < buffer_time and item['status'].lower() == 'confirmado':
                        return JSONResponse(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            content={
                                "message": "Conflicto de reservas: ya existe una reserva cercana para esta mesa."
                            }
                        )
                        
            await ReservationModel.update_reservation(id, data)
            
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "message": "Reserva actualizada exitosamente."
                }
            )

            
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def delete_reservation(id : int | str, user : dict):
        try:
            user_response = await UserModel.get_user_by_ID(user['user_ID'])
            if not user_response:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'Usuario no encontrado'
                    }
                )
            
            existing_reservation = await ReservationModel.get_reservation(id)
            
            if not existing_reservation:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'Reserva a eliminar no encontrada'
                    }
                )
                
            if existing_reservation['user_ID'] != user['user_ID']:
                return JSONResponse(
                    status_code = status.HTTP_403_FORBIDDEN,
                    content = {
                        'message' : 'No tienes permiso para eliminar esta reserva'
                    }
                )
        
            await ReservationModel.delete_reservation(id, user['user_ID'])
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Reserva eliminada correctamente'
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def verify_reservations(user : dict):
        try:      
            not_admin = await is_user_admin(user['role_ID'])
            if not_admin:
                return not_admin
            
            all_reservations = await ReservationModel.get_reservations()
            today = datetime.now()
            
            for reservation in all_reservations:
                # Obtén la fecha y hora de la reserva
                reservation_date = reservation['reservation_date']
                reservation_time = reservation['reservation_time']
                
                # Combina la fecha y hora de la reserva
                reservation_datetime = datetime.combine( 
                    reservation_date, datetime.min.time()
                ) + reservation_time
                
                # Verifica si la reserva está en el pasado
                if reservation_datetime < today:
                    await ReservationModel.update_status(
                        reservation['reservation_ID'], 'finalizado'
                    )
                    
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Todas las reservas existentes fueron validadas'
                }
            )        
             
        except Exception as err:
            return await handle_exception(err)