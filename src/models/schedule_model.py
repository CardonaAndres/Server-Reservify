from src.schemas.schedule_schema import ScheduleSchema
from src.utils.database import db_connection
import aiomysql

class ScheduleModel:
    @staticmethod
    async def get_schedule_full():
        try:
            
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM schedules")
                result = await cursor.fetchall()
                return result
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            return []  
          
        except Exception as e:
            
            print(f"Error al obtener el horario: {e}")
            return None
        
        finally:
            if conn:
                conn.close()
                
    @staticmethod
    async def get_schedule_day(id : int | str):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute('SELECT * FROM schedules WHERE schedule_ID = %s', (id,))
                return await cursor.fetchone()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise  
            
        except Exception as err:
            print(f"Error al obtener el horario: {err}")
            raise  
        finally:
            if conn:
                conn.close()
                
    @staticmethod
    async def register_day(data : ScheduleSchema):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """INSERT INTO schedules (weekday, open_time, close_time)
                    VALUES (%s, %s, %s)""", ( data.weekday, data.open_time, data.close_time) 
                )
                await conn.commit()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            await conn.rollback()
            print(f"Error en la base de datos: {str(err)}")
            raise
        
        except Exception as err:
            await conn.rollback()
            print(str(err))
            raise
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    async def update_day(data : ScheduleSchema, id : str | int):
        try :
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """UPDATE schedules SET weekday = %s, open_time = %s, close_time = %s 
                       WHERE schedule_ID = %s""", 
                    (data.weekday, data.open_time, data.close_time, id)
                )
                
            await conn.commit()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            await conn.rollback()
            print(f"Error en la base de datos: {str(err)}")
            return None
        except Exception as err :
            print(str(err))
            return None
        
        finally:
            if conn:
                conn.close()   
    
    @staticmethod
    async def delete_day(id : str | int):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("DELETE FROM schedules WHERE schedule_ID = %s", (id,))
                
            await conn.commit()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
        
        except Exception as err :
            print(str(err))
            raise
        
        finally:
            if conn:
                conn.close()    
                
                