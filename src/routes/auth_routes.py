from fastapi import APIRouter
from src.controllers.auth_controller import AuthController
from src.schemas.auth_schema import LoginSchema, RegisterSchema, UpdatePasswordSchema

auth_router = APIRouter(prefix='/auth', tags=['Auth'])

@auth_router.post('/login')
async def login(user_data : LoginSchema):
     return await AuthController.login(user_data)
 
@auth_router.post('/register')
async def register(user_data : RegisterSchema):
     return await AuthController.register(user_data)

@auth_router.put('/update-password')
async def update_password(data : UpdatePasswordSchema):
     return await AuthController.update_password(data)

@auth_router.post('/logout')
async def logout():
     return await AuthController.logout()


