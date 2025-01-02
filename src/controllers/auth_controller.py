from fastapi import status, Depends
from fastapi.responses import JSONResponse
from src.models.auth_model import AuthModel
from src.models.user_model import UserModel
from src.schemas.auth_schema import LoginSchema, RegisterSchema, UpdatePasswordSchema
from src.utils.handle_exception import handle_exception
from src.libs.jwt import create_token_user
from src.utils.verify_token import verify_token
from datetime import timedelta
import bcrypt
import re

class AuthController:
    @staticmethod
    async def login(user_data : LoginSchema):
        try:
            existing_user = await AuthModel.get_user_by_email(user_data.email)
            user_password = user_data.password
            
            if not existing_user:
                    return JSONResponse(
                        status_code = status.HTTP_404_NOT_FOUND, 
                        content={ 'message' : 'El correo no se encuentra registrado' }
                    )   
                    
            password_is_correct = bcrypt.checkpw(
                user_password.encode('utf-8'), existing_user['password'].encode('utf-8')
            )
            
            if not password_is_correct:
                    return JSONResponse(
                        status_code=401, 
                        content={ 'message': 'Contraseña incorrecta' }
                    )
                    
            token = await create_token_user(
                RegisterSchema(
                    name = existing_user['name'],
                    email = existing_user['email'],
                    cellphone = existing_user['cellphone'],
                    password = existing_user['password'],
                    role_ID = existing_user['role_ID'],
                ), user_ID = existing_user['user_ID']  
            )
                    
            end_response = JSONResponse(status_code=status.HTTP_200_OK, 
                content={ 'message' : 'Bienvenido',
                'user' : {
                    'user_ID' : existing_user['user_ID'],
                    'email' : existing_user['email'],
                    'cellphone' : existing_user['cellphone'],
                    'role_ID' : existing_user['role_ID']
                }, 
                'token' : token     
            })
            
            end_response.set_cookie(
                    key="token",
                    value=token,
                    httponly=True,  # No accesible desde JavaScript
                    secure=False,  # Cambiar a True si usas HTTPS
                    max_age=timedelta(days=1),
                    expires=timedelta(days=1),  # Define la expiración explícitamente
                    path = '/'
                )
                
            return end_response
                
        except Exception as err:
           return await handle_exception(err)
     
    @staticmethod   
    async def register(user_data : RegisterSchema):
        # Registra un nuevo usuario después de realizar las validaciones necesarias.
        try:
            existing_user = await AuthModel.get_user_by_email(user_data.email)
            existing_cellphone = await UserModel.get_user_by_cellphone(user_data.cellphone)

            if existing_user:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    content={ 'message' : 'El usuario ya está registrado con este correo electrónico.'}
                )
                
            if existing_cellphone:
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    content={ 'message' : 'El usuario ya está registrado con este número de teléfono.'}
                )
                
            hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())
            
            new_user = RegisterSchema(
                name = user_data.name,
                email = user_data.email,
                cellphone = user_data.cellphone,
                password = hashed_password,
                role_ID = user_data.role_ID
            )
            
            await AuthModel.register(new_user)
            
            user = await AuthModel.get_user_by_email(user_data.email)         
            token = await create_token_user(new_user, user['user_ID'])
            
            if not token:
                return JSONResponse(
                    status_code = status.HTTP_400_BAD_REQUEST, 
                    content = {"message": "Error al generar el token"}
                )
                
            
            end_response = JSONResponse(status_code=201, content={
                'message' : 'Registrado con exito',
                'user' : {
                    'user_ID' : user['user_ID'],
                    'email' : user['email'],
                    'cellphone' : user['cellphone'],
                    'role_ID' : user['role_ID']
                },
                'token' : token,
            })
            
            end_response.set_cookie(
                key="token",
                value=token,
                httponly=True,  # No accesible desde JavaScript
                secure=False,  # Cambiar a True si usas HTTPS
                max_age=timedelta(days=1),
                expires=timedelta(days=1),  # Define la expiración explícitamente
                path = '/'
            )
            
            return end_response
                
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def update_password(data : UpdatePasswordSchema):
        try:
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            
            if not re.match(email_regex, data.email):
                return JSONResponse(
                    status_code = 400,
                    content = {
                        'message' : 'El formato del email es inválido.'
                    }
                )
                
            existing_user = await AuthModel.get_user_by_email(data.email)
            
            if not existing_user:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'El correo no se encuentra registrado.'
                    }
                )
                            
            is_same_password = bcrypt.checkpw(
                data.new_password.encode('utf-8'), existing_user['password'].encode('utf-8')
            )
            
            if is_same_password:
                return JSONResponse(
                    status_code = 400,
                    content = {
                        'message' : 'La nueva contraseña no puede ser igual a la anterior.'
                    }
                )
                
            hashed_password = bcrypt.hashpw(data.new_password.encode('utf-8'), bcrypt.gensalt())
            data.new_password = hashed_password
                
            await AuthModel.update_password(data)
         
            return JSONResponse(
                status_code = status.HTTP_200_OK, 
                content = { 
                    'message' : 'Contraseña cambiada correctamente' 
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
     
    @staticmethod   
    async def logout():
        try:
            response = JSONResponse(
                status_code=status.HTTP_200_OK, 
                content={ 'message' : 'Sesión cerrada correctamente' }
            )
            
            response.delete_cookie('token')
            
            return response
    
        except Exception as err:
            return await handle_exception(err)
        
    @staticmethod
    async def verify_session(user : dict):
        try:
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Sesión válida',
                    'user' : user
                } 
            )
        except Exception as err:
            return await handle_exception(err)