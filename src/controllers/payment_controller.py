from fastapi import status
from fastapi.responses import JSONResponse
from src.schemas.payment_schema import PaymentSchema
from src.models.reservation_model import ReservationModel
from src.models.payment_model import PaymentModel
from src.utils.handle_exception import handle_exception
from src.utils.reservation_helpers import convert_timedelta_to_time
from src.utils.payment_herlpers import format_ticket_payment, format_tickets_payments
from src.utils.is_admin import is_user_admin
from datetime import datetime, timedelta
import random

class PaymentController:
    @staticmethod
    async def get_all_payments(user : dict, page : int = 1):
        try:
            not_user_admin = await is_user_admin(user['role_ID'])
            if not_user_admin:
                return not_user_admin
            
            tickets_info = await PaymentModel.get_payments_paginate(page)
            tickets_info['tickets'] = format_tickets_payments(tickets_info['tickets']) 
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = tickets_info             
            )           
            
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def get_payment(reservation_ID : int | str, user : dict):
        try:
            ticket = await PaymentModel.get_payment(reservation_ID, user['user_ID'])
            
            if not ticket:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'Recibo no encontrado'
                    }
                )    
                                  
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = format_ticket_payment(ticket)    
            )
            
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def do_payment(data : PaymentSchema, user : dict):
        try:
            reservation = await ReservationModel.get_reservation(user['user_ID'], data.reservation_ID)
            all_payments = await PaymentModel.get_all_payments()
            payment_methods  = ["nequi", "daviplata", "bancolombia a la mano", "bancolombia personas"]
            transfer_status = ["Completada", "Fallida"]
            
            if data.payment_method.lower() not in payment_methods:
                return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    content = {
                        'message' : 'El metodo de pago seleccionado no es valido'
                    }
                )
                

            if not reservation:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'La reserva a la cual quiere hacer el pago no existe'
                    }
                )
                
            for payment in all_payments:
                if payment['reservation_ID'] == data.reservation_ID:
                    return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        content = {
                            'message' : 'La reserva ya tiene un pago registrado'
                        }
                    )
                
            # Simulación del proceso de pago
            payment_status = random.choice(transfer_status)
            
            if payment_status == transfer_status[0]:
                
                data.status = payment_status
                await PaymentModel.do_payment(data)
                await ReservationModel.update_status(
                    reservation['reservation_ID'], new_status = "confirmada"
                )
                
                buffer_time = timedelta(minutes=40)
                reservation_confirmed = datetime.combine(
                    reservation['reservation_date'], 
                    convert_timedelta_to_time(reservation['reservation_time'])
                )
                
                reservations = await ReservationModel.get_reservations()
                
                for res in reservations:
                    # Excluir la reserva propia para que no sea eliminada
                    if res['reservation_ID'] == reservation['reservation_ID']:
                        continue
                    
                    if res['reservation_date'] == reservation['reservation_date']:
                        res_time = datetime.combine(
                            res['reservation_date'], convert_timedelta_to_time(res['reservation_time'])
                        )
                        
                        if (reservation_confirmed >= res_time >= reservation_confirmed - buffer_time and
                            res['status'] == 'pendiente' ):
                            await ReservationModel.delete_reservation(
                                id = res['reservation_ID'], user_ID = res['user_ID']
                            )
                            
                
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={
                            'message': 'Pago realizado con éxito',
                            'payment_status': payment_status,
                            'payment_method': data.payment_method,
                            'amount': str(data.amount)
                    }
                )
                
            # Si la transferencia no es completada, simula fallo o cancelación
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    'message': f'El pago no se pudo procesar, estado de transferencia: {payment_status}',
                    'payment_status': payment_status
                }
            )           
            
        except Exception as err:
            return await handle_exception(err)