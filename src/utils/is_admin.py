from fastapi import status
from fastapi.responses import JSONResponse

async def is_user_admin(user_role_ID : str | int):
    try:
        # Convertir el rol a entero y verificar
        if int(user_role_ID) != 1:
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={'message': 'No tienes permisos para realizar esta acción'}
            )
            
    except ValueError:
        # Respuesta si el rol no es un número válido
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'message': 'ID de rol no válido'}
        )
    
    # Si el usuario es administrador, no retorna nada (permitido)
    return None
