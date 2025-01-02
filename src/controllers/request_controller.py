from fastapi.responses import JSONResponse    
from fastapi import status
from src.models.request_model import ServiceRequestModel
from src.models.user_model import UserModel
from src.utils.handle_exception import handle_exception
from src.schemas.request_schema import ServiceRequestSchema
from src.utils.is_admin import is_user_admin

class ServiceRequestController:
    @staticmethod
    async def get_all_requests(user : dict, page : int = 1):
        try:
            not_admin = await is_user_admin(user['role_ID'])
            if not_admin:
                return not_admin
            
            requests = await ServiceRequestModel.get_all_requests_paginate(page)
            
            for request in requests['requests']:
                for key, value in request.items():
                    if key == 'created_at' or key == 'user_created_at':
                        request[key] = str(value)
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = requests
            )
            
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def get_my_requests(user : dict, page : int = 1):
        try:
            requests = await ServiceRequestModel.get_my_requests(user['user_ID'], page)
            
            for request in requests['requests']:
                for key, value in request.items():
                    if key == 'created_at':
                        request[key] = str(value)
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = requests
            )
            
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def create_request(user : dict, data : ServiceRequestSchema):
        try:
            verify_user = await UserModel.get_user_by_ID(user['user_ID'])
            
            if not verify_user:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = "Usuario no encontrado"
                )
            
            data.user_ID = user['user_ID']
            
            await ServiceRequestModel.create_request(data)
            
            return JSONResponse(
                status_code = status.HTTP_201_CREATED,
                content = {
                    "message" : "Solicitud creada exitosamente"
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
        