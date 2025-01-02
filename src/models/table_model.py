from src.utils.database import db_connection
from src.schemas.table_schema import TableSchema
import aiomysql

class TableModel:
    @staticmethod
    async def get_all_tables_paginate(page: int = 1):
        try:
            # Calcula el OFFSET basado en la página
            offset = (page - 1) * 10
            
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                
                await cursor.execute(
                    "SELECT * FROM tables LIMIT %s OFFSET %s", (10, offset)
                )
                
                result = await cursor.fetchall()

                await cursor.execute("SELECT COUNT(*) AS total FROM tables")
                
                total_result = await cursor.fetchone()
                total_pages = (total_result['total'] + 10 - 1) // 10

                return {
                    "tables": result,
                    "total_count": total_result['total'],
                    "total_pages": total_pages,
                    "current_page": page
                }
        
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
          
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    async def get_all_tables():   
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute('SELECT * FROM tables')
                return await cursor.fetchall()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
          
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise
        
        finally:
            if conn:
                conn.close()
                
    @staticmethod
    async def get_table(id : int | str):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute('SELECT * FROM tables WHERE table_ID = %s', (id, ))
                return await cursor.fetchone()
            
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            print(f"Error en la base de datos: {str(err)}")
            raise
          
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise
        
        finally:
            if conn:
                conn.close()
    
    @staticmethod
    async def resgister_table(data : TableSchema):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "INSERT INTO tables (table_number, capacity) VALUES (%s, %s)",
                    (data.table_number, data.capacity)
                )
                await conn.commit()
              
        except aiomysql.Error as err:
            # Manejo de errores relacionados con MySQL
            await conn.rollback()
            print(f"Error en la base de datos: {str(err)}")
            raise  
          
        except Exception as e:
            # Manejo de otros errores
            print(f"Error al obtener los datos: {e}")
            raise  
        
        finally:
            if conn:
                conn.close()          

    @staticmethod
    async def update_table(id: int | str, data : TableSchema):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """UPDATE tables SET table_number = %s, capacity = %s WHERE table_ID = %s
                    """, (data.table_number, data.capacity, id)
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
        finally:
            if conn:
                conn.close()    
        
    @staticmethod
    async def delete_table(id : int | str):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "DELETE FROM tables WHERE table_ID = %s",
                    (id,)
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
        finally:
            if conn:
                conn.close()