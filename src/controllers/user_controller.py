from fastapi.responses import JSONResponse
from fastapi import status
from src.models.user_model import UserModel
from src.models.auth_model import AuthModel
from src.utils.handle_exception import handle_exception
from src.utils.is_admin import is_user_admin
from src.schemas.user_schema import ChangeRoleSchema, UpdateUserSchema

class UserController:
    @staticmethod
    async def get_all_users(user : dict, page : int = 1):
        
        try:
            
            is_not_user_admin = await is_user_admin(user['role_ID'])
            if is_not_user_admin:
                return is_not_user_admin
            
            users = await UserModel.get_all_users_paginate(page)
            
            for user in users['users']:
                for key, value in user.items():
                    if key == 'created_at':
                        user[key] = str(value)

            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = users
            )
                    
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def get_user_by_email(email : str, user : dict):
        try:
            not_admin = await is_user_admin(user['role_ID'])
            if not_admin:
                return not_admin
            
            user = await AuthModel.get_user_by_email(email)
            if not user:
                return  JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'El usuario con el correo dado no ha sido encontrado.'
                    }
                )
                
            del user['password']
            user['created_at'] = str(user['created_at'])
                
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Usuario encontrado',
                    'user' : user
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def get_profile(user : dict):
        try:
            user_data = await UserModel.get_user_by_ID(user['user_ID'])
            
            if not user_data:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        "message" : "El usuario no existe."
                    }
                )
            
            user_data['created_at'] = str(user_data['created_at'])
            del user_data['password']
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = user_data
            )
        
        except Exception as err:
            return await handle_exception(err)
    
    @staticmethod
    async def change_role(user : dict, data : ChangeRoleSchema):
        try:
            is_not_user_admin = await is_user_admin(user['role_ID'])
            roles_available = [1, 2]
            
            if is_not_user_admin:
                return is_not_user_admin
            
            existing_user = await AuthModel.get_user_by_email(data.email)
            
            if not existing_user:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        "message" : "El usuario al cual desea cambiar el rol no existe."
                    }
                )
            
            if data.role_ID not in roles_available:
                return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    content = {
                        "message" : "El rol seleccionado no es válido."
                    }
                )
                
            await UserModel.change_user_role(data)
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    "message" : "El rol del usuario ha sido cambiado exitosamente."
                }
            )
        
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def update_user(user : dict, data : UpdateUserSchema):
        try:
            email_exists = await AuthModel.get_user_by_email(data.email)
            cellphone_exists = await UserModel.get_user_by_cellphone(data.cellphone)
            
            if email_exists and email_exists['user_ID'] != user['user_ID']:
                return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    content = {
                        "message" : "El correo electrónico ya está en uso."
                    }
                )
                
            if cellphone_exists and cellphone_exists['user_ID'] != user['user_ID']:
                return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    content = {
                        "message" : "El número de teléfono ya está en uso."
                    }
                )

            await UserModel.update_user(user['user_ID'], data)
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    "message" : "Los datos del usuario han sido actualizados exitosamente."
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
        