from fastapi import APIRouter, Depends, Query
from src.schemas.table_schema import TableSchema
from src.controllers.tables_controller import TableController
from src.utils.verify_token import verify_token

table_router = APIRouter(prefix='/tables', tags=['Tables'])

@table_router.get('/tables')
async def get_tables(page: int = Query(1, ge=1)):
    return await TableController.get_all_tables(page)

@table_router.get('/table/{id}')
async def get_table(id : str | int):
    return await TableController.get_table(id)

@table_router.post('/table')
async def register_table(data : TableSchema, user : dict = Depends(verify_token)):
    return await TableController.register_table(data, user)

@table_router.put('/table/{id}')
async def update_table(id : str | int, data : TableSchema, user : dict = Depends(verify_token)):
    return await TableController.update_table(id, data, user)

@table_router.delete('/table/{id}')
async def delete_table(id : str | int, user : dict = Depends(verify_token)):
    return await TableController.delete_table(id, user)