from src.utils.database import db_connection
from src.schemas.request_schema import ServiceRequestSchema
import aiomysql

class ServiceRequestModel:
    @staticmethod
    async def get_all_requests_paginate(page : int = 1):
        try:
            conn = await db_connection()
            offset = (page - 1) * 15
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                await cursor.execute(
                    """
                        SELECT r.role_name, u.name, u.email, u.cellphone, 
                        u.created_at AS user_created_at, u.role_ID, sr.* FROM roles r 
                        INNER JOIN users u ON r.role_ID = u.role_ID
                        INNER JOIN service_requests sr ON u.user_ID = sr.user_ID LIMIT 15 OFFSET %s
                    """, (offset,)
                )
                
                result = await cursor.fetchall()
                
                await cursor.execute(
                    "SELECT COUNT(*) AS total FROM service_requests",
                )
                
                total_result = await cursor.fetchone()
                total_pages = (total_result['total'] + 15 - 1) // 15
                
                return {
                    'requests' : result,
                    'total_count' : total_result['total'],
                    'total_pages' : total_pages,
                    'current_page': page
                }
                
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
          
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise
        
    @staticmethod
    async def get_my_requests(user_ID : int, page : int = 1):
        try:
            conn = await db_connection()
            offset = (page - 1) * 15
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                await cursor.execute(
                    "SELECT * FROM service_requests WHERE user_ID = %s LIMIT 15 OFFSET %s", 
                    (user_ID, offset)
                )
                
                result = await cursor.fetchall()
                
                await cursor.execute(
                    "SELECT COUNT(*) AS total FROM service_requests WHERE user_ID = %s",
                    (user_ID,)
                )
                
                total_result = await cursor.fetchone()
                total_pages = (total_result['total'] + 15 - 1) // 15
                
                return {
                    'requests' : result,
                    'total_count' : total_result['total'],
                    'total_pages' : total_pages,
                    'current_page': page
                }
                
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
          
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise

    @staticmethod
    async def create_request(data : ServiceRequestSchema):
        try:
            conn = await db_connection()
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                await cursor.execute(
                    """
                        INSERT INTO service_requests (title, description, user_ID) 
                        VALUES (%s, %s, %s)
                    """, (data.title, data.description, data.user_ID)
                )
                
                await conn.commit()
                
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            await conn.rollback()
            print(f"Error en la base de datos: {str(err)}")
            raise
          
        except Exception as e:
            # Manejo de otros errores
            await conn.rollback()
            print(f"Error al obtener los datos: {e}")
            raise