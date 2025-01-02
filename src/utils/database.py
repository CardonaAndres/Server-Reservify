import aiomysql as sql_manager
from src.configs.config import db_config

async def db_connection():
    try:
        return await sql_manager.connect(**db_config)
    except Exception as err:
        raise ValueError(f"No se ha podido conectar a la base de datos: {str(err)}")
