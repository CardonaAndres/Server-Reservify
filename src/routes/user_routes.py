from fastapi import APIRouter, Depends, Query
from src.controllers.user_controller import UserController
from src.utils.verify_token import verify_token
from src.schemas.user_schema import ChangeRoleSchema, UpdateUserSchema

user_router = APIRouter(prefix = "/users", tags = ["Users"])

@user_router.get("/users")
async def get_all_users(page : int = Query(1, gt = 0), user : dict = Depends(verify_token)):
    return await UserController.get_all_users(user, page)

@user_router.get("/profile")
async def get_profile(user : dict = Depends(verify_token)):
    return await UserController.get_profile(user)

@user_router.get('/user-by-email/{email}')
async def get_user_by_email(email : str, user : dict = Depends(verify_token)):
    return await UserController.get_user_by_email(email, user)

@user_router.put("/change-role")
async def change_role(data : ChangeRoleSchema, user : dict = Depends(verify_token) ):
    return await UserController.change_role(user, data)

@user_router.put("/update")
async def update_user(data : UpdateUserSchema, user : dict = Depends(verify_token)):
    return await UserController.update_user(user, data)


