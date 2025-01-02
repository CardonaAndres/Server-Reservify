from src.utils.database import db_connection
from src.schemas.payment_schema import PaymentSchema
import aiomysql

class PaymentModel:
    @staticmethod
    async def do_payment(data : PaymentSchema):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """INSERT INTO payments (reservation_ID, amount, payment_method, status) 
                       VALUES (%s, %s, %s, %s)""", (
                           data.reservation_ID, data.amount, data.payment_method, data.status
                    )
                )
                
                await conn.commit()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
        
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise
        
    @staticmethod
    async def get_payment(reservation_ID : int | str):
        try:
            conn = await db_connection()
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:         
                       
                await cursor.execute(
                    """ 
                        SELECT u.name, u.email, u.cellphone, r.*, p.payment_ID, 
                        p.amount, p.payment_method, p.status as payment_status, p.paid_at 
                        FROM users u INNER JOIN reservations r ON u.user_ID = r.user_ID 
                        INNER JOIN payments p ON r.reservation_ID = p.reservation_ID 
                        WHERE r.reservation_ID = %s  
                    """, 
                    (reservation_ID)
                )            
                
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
    async def get_payments_paginate(page : int = 1):
        try:
            conn = await db_connection() 
            offset = (page - 1) * 10
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                        SELECT u.name, u.email, u.cellphone, r.*, p.payment_ID, 
                        p.amount, p.payment_method, p.status as payment_status, p.paid_at 
                        FROM users u INNER JOIN reservations r ON u.user_ID = r.user_ID 
                        INNER JOIN payments p ON r.reservation_ID = p.reservation_ID 
                        LIMIT %s OFFSET %s                             
                    """, 
                    (10, offset)
                )
                
                result = await cursor.fetchall()
                
                await cursor.execute("SELECT COUNT(*) AS total FROM payments")
                
                total_result = await cursor.fetchone()
                total_pages = (total_result['total'] + 10 - 1) // 10
                
                return {
                    'tickets' : result,
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
    async def get_all_payments():
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM payments")
                return await cursor.fetchall()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
        
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise