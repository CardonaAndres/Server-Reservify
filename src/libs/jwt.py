import jwt
from datetime import datetime, timedelta
from src.configs.config import SECRET_KEY, ALGORITHM
from src.schemas.auth_schema import RegisterSchema

async def create_token_user(user_data : RegisterSchema, user_ID : int):
    
    expiration_time = datetime.utcnow() + timedelta(hours=1)
     
    payload = {
        'user_ID' : user_ID,
        'email' : user_data.email, 
        'role_ID' : user_data.role_ID,
        'exp': expiration_time
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token