from src.schemas.user_schema import ChangeRoleSchema, UpdateUserSchema
from src.utils.database import db_connection
import aiomysql

class UserModel:
    @staticmethod
    async def get_user_by_ID(id : int | str):
        #Busca un usuario por el ID
        conn = await db_connection()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM users WHERE user_ID = %s", (id))
                result = await cursor.fetchone()
                if result:
                    return result
                
                return None
            
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
    async def get_user_by_cellphone(cellphone : str):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM users WHERE cellphone = %s", (cellphone))
                result = await cursor.fetchone()
                if result:
                    return result
                
                return None
            
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
    async def get_all_users_paginate(page : int = 1):
        try:
            conn = await db_connection()
            offset = (page - 1) * 10
            
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """SELECT r.role_name, u.user_ID, u.name, u.email, 
                       u.cellphone, u.created_at, u.role_ID FROM users u
                       INNER JOIN roles r ON r.role_ID = u.role_ID LIMIT %s OFFSET %s
                    """,
                    (10, offset)
                )
                
                result = await cursor.fetchall()
                
                await cursor.execute("SELECT COUNT(*) as total FROM users")
                total_result = await cursor.fetchone()
                total_pages = (total_result['total'] + 10 - 1) // 10
                
                return {
                    'users' : result,
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
                        
        finally:
            if conn:
                conn.close()
                
                
    @staticmethod
    async def update_user(user_ID : int | str, data : UpdateUserSchema):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "UPDATE users SET name = %s, email = %s, cellphone = %s WHERE user_ID = %s",
                    (data.name, data.email, data.cellphone, user_ID)
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
                        
        finally:
            if conn:
                conn.close()
            
    @staticmethod
    async def change_user_role(data : ChangeRoleSchema):
        try:
            conn = await db_connection()
            
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "UPDATE users SET role_ID = %s WHERE email = %s",
                    (data.role_ID, data.email)
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
                        
        finally:
            if conn:
                conn.close()    