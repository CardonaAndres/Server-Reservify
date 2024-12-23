from src.configs.config import SECRET_KEY, ALGORITHM
from fastapi import HTTPException, Request, status
from src.models.user_model import UserModel
from jwt.exceptions import PyJWTError
import jwt
import logging

async def verify_token(req : Request):
    # Obtiene el token de las cookies
    token = req.cookies.get("token")
    
    if not token:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED, 
            detail="Autorización denegada. Por favor, iniciar sesión"
        )
    
    try:
        # Verifica el token con la clave secreta
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM], options = {
                'verify_signature': True, 'require_exp': True, 'verify_exp': True
            }
        )

        # Asegúrate de que el token contiene el campo 'email'
        if 'user_ID' not in payload:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED, 
                detail = "Estructura de token inválida"
            )
        
        # Obtiene el usuario desde la base de datos
        user = await UserModel.get_user_by_ID(payload['user_ID'])
        
        if not user:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED, 
                detail = "Usuario no encontrado"
            )
        
        return {
            'user_ID' : user['user_ID'],
            'email' : user['email'],
            'cellphone' : user['cellphone'],
            'role_ID' : user['role_ID']
        }
    
    except jwt.ExpiredSignatureError:
        # Token caducado
        logging.warning("Token ha expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail = "Por favor, inicie sesión nuevamente."
        )
    
    except (jwt.InvalidTokenError, PyJWTError) as token_error:
        # Token inválido o manipulado
        logging.error(f"Error de validación de token: {str(token_error)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Token de autenticación inválido o alterado"
        )
        
    except Exception as e:
        # Registro detallado del error
        logging.critical(f"Error inesperado en verificación de token: {str(e)}")
        
        # Manejo genérico para cualquier otro error inesperado
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail = f"Error interno del sistema. Por favor, contacte con soporte."
        )