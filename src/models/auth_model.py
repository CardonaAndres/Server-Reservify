from src.schemas.auth_schema import RegisterSchema, UpdatePasswordSchema
from src.utils.database import db_connection
import aiomysql

class AuthModel:
    @staticmethod
    async def register(user_data : RegisterSchema):
        #Agrega un nuevo usuario a la base de datos.
        conn = await db_connection()
        try:
            
            async with conn.cursor() as cursor:
                query = """INSERT INTO users (name, email, cellphone, password, created_at, role_ID) 
                            VALUES (%s, %s, %s, %s, NOW(), %s)"""  
                            
                await cursor.execute(
                    query, (
                        user_data.name, 
                        user_data.email, 
                        user_data.cellphone, 
                        user_data.password,
                        user_data.role_ID
                    )
                )
                
                await conn.commit()
        except Exception as e:
            await conn.rollback()
            raise e
        finally:
            conn.close() 
            
    @staticmethod
    async def get_user_by_email(email : str):
        #Busca un usuario por correo electrónico
        conn = await db_connection()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute("SELECT * FROM users WHERE email = %s", (email))
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
    async def update_password(data : UpdatePasswordSchema):
        try:
            conn = await db_connection()
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    "UPDATE users SET password = %s WHERE email = %s",
                    (data.new_password, data.email)                              
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