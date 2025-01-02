from fastapi import status
from fastapi.responses import JSONResponse

async def handle_exception(err):
    #Maneja las excepciones generando respuestas estandarizadas.
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={'message': f'Error interno en el servidor: {str(err)}'}
    )