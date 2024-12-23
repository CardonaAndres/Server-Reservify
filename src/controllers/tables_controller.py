from fastapi.responses import JSONResponse
from fastapi import status
from src.utils.is_admin import is_user_admin
from src.models.table_model import TableModel
from src.utils.handle_exception import handle_exception
from src.schemas.table_schema import TableSchema


class TableController:
    @staticmethod
    async def get_all_tables(page : int = 1):
        try:
            tables = await TableModel.get_all_tables_paginate(page)
           
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Todas las mesas encontradas',
                    'tables' : tables
                }       
            )
            
        except Exception as err:
            return await handle_exception(err)
            
    @staticmethod
    async def get_table(id : int | str):
        try:
            table = await TableModel.get_table(id)
            
            if not table:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'No se ha encontrado la mesa'
                    }
                )
                
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = table
            )
            
        except Exception as err:
            return await handle_exception(err)
            
    @staticmethod
    async def register_table(data : TableSchema, user : dict):
        try:
            not_admin = await is_user_admin(user['role_ID'])
            tables = await TableModel.get_all_tables()
            
            if not_admin:
                return not_admin
            
            for table in tables:
                if table['table_number'] == data.table_number:
                    return JSONResponse(
                        status_code = status.HTTP_400_BAD_REQUEST,
                        content = {
                            'message' : 'La mesa ya se encuentra registrada'
                        }
                    )
            
            await TableModel.resgister_table(data)
            
            return JSONResponse(
                status_code = status.HTTP_201_CREATED,
                content = {
                    'message' : 'Mesa registrada con exito'
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
                      
    @staticmethod
    async def update_table(id : int | str, data : TableSchema, user : dict):
        try:
            not_admin = await is_user_admin(user['role_ID'])
            table = await TableModel.get_table(id)
            
            if not_admin:
                return not_admin
            
            if not table:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'La mesa con el ID dado no ha sido encontrada'
                    }
                )
                
            await TableModel.update_table(id, data)
            
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Actualizado correctamente'
                }
            )
            
        except Exception as err:
            return await handle_exception(err)
            
    @staticmethod
    async def delete_table(id : int | str, user : dict):
        try:
            not_admin = await is_user_admin(user['role_ID'])
            table = await TableModel.get_table(id)
            
            if not_admin:
                return not_admin
        
            if not table:
                return JSONResponse(
                    status_code = status.HTTP_404_NOT_FOUND,
                    content = {
                        'message' : 'Mesa a eliminar no encontrada'
                    }
                )
                
            await TableModel.delete_table(id)
                     
            return JSONResponse(
                status_code = status.HTTP_200_OK,
                content = {
                    'message' : 'Mesa eliminada correctamente'
                }
            )
              
        except Exception as err:
            return await handle_exception(err)