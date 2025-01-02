from src.utils.database import db_connection
from src.schemas.reservation_schema import ReservationSchema
import aiomysql

class ReservationModel:
    @staticmethod
    async def get_all_reservations_admin(page : int = 1):
        try:
            conn = await db_connection()
            offset = (page - 1) * 10
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                query = '''SELECT r.*, t.table_number, t.capacity FROM reservations r 
                           INNER JOIN tables t ON t.table_ID = r.table_ID LIMIT %s OFFSET %s'''
                           
                await cursor.execute(query, (10, offset))
                
                result = await cursor.fetchall()
                
                await cursor.execute("SELECT COUNT(*) AS total FROM reservations")
                
                total_result = await cursor.fetchone()
                total_pages = (total_result['total'] + 10 - 1) // 10

                return {
                    'reservations' : result,
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
    async def get_reservations_paginate(user_ID : int | str, page : int = 1):
        try:
            conn = await db_connection()
            offset = (page - 1) * 10
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                query = '''SELECT r.*, t.table_number, t.capacity FROM reservations r 
                           INNER JOIN tables t ON t.table_ID = r.table_ID 
                           WHERE r.user_ID = %s LIMIT %s OFFSET %s'''
                           
                await cursor.execute(query, (user_ID, 10, offset))
                
                result = await cursor.fetchall()
                
                await cursor.execute(
                    "SELECT COUNT(*) AS total FROM reservations WHERE user_ID = %s",
                    (user_ID,)
                )
                
                total_result = await cursor.fetchone()
                total_pages = (total_result['total'] + 10 - 1) // 10

                return {
                    'reservations' : result,
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
    async def get_reservation(id : int | str):
        try:
            conn = await db_connection()

            async with conn.cursor(aiomysql.DictCursor) as cursor:
                query = """SELECT r.*, t.table_number, t.capacity
                           FROM reservations r INNER JOIN tables t ON t.table_ID = r.table_ID 
                           WHERE r.reservation_ID = %s"""
                
                await cursor.execute(query, (id))
                return await cursor.fetchone()          
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
          
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise
        
    @staticmethod
    async def get_reservations():
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM reservations")
                return await cursor.fetchall()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
        
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise
         
    @staticmethod
    async def create_reservation(data : ReservationSchema):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                reservation_time_str = data.reservation_time.strftime("%H:%M")
               
                await cursor.execute(
                    """INSERT INTO reservations (reservation_date, reservation_time, status, user_ID, table_ID) VALUES (%s, %s, %s, %s, %s)""", 
                    (data.reservation_date, reservation_time_str, data.status, data.user_ID, 
                     data.table_ID )
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
        
    @staticmethod
    async def update_reservation(id : int | str, data : ReservationSchema):
        try:
            conn = await db_connection()
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                reservation_time_str = data.reservation_time.strftime("%H:%M")
                
                await cursor.execute(
                    """UPDATE reservations set reservation_date = %s, 
                       reservation_time = %s, status = %s, user_ID = %s, table_ID = %s
                       WHERE reservation_ID = %s
                    """, (data.reservation_date, reservation_time_str, data.status, data.user_ID, 
                          data.table_ID, id)
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
        
    @staticmethod
    async def update_status(id : int | str, new_status : str):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "UPDATE reservations SET status = %s WHERE reservation_ID = %s",
                    (new_status, id)
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
        
    @staticmethod
    async def delete_reservation(id: int | str, user_ID : int):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "DELETE FROM reservations WHERE reservation_ID = %s AND user_ID = %s",
                    (id, user_ID)
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
        