from fastapi import APIRouter, Depends, Query
from src.utils.verify_token import verify_token
from src.controllers.request_controller import ServiceRequestController
from src.schemas.request_schema import ServiceRequestSchema

request_router = APIRouter(prefix="/requests", tags=["Request"])

@request_router.get("/requests")
async def get_all_requests(user : str = Depends(verify_token), page : int = Query(1, gt = 0)):
    return await ServiceRequestController.get_all_requests(user, page)

@request_router.get("/my-requests")
async def get_my_requests(user : str = Depends(verify_token), page : int = Query(1, gt = 0)):
    return await ServiceRequestController.get_my_requests(user, page)

@request_router.post("/request")
async def create_request(data : ServiceRequestSchema, user : str = Depends(verify_token)):
    return await ServiceRequestController.create_request(user, data)