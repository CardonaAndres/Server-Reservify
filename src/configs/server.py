from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth_routes import auth_router
from src.routes.schedule_routes import schedule_router
from src.routes.table_routes import table_router
from src.routes.reservation_routes import reservation_router
from src.routes.payment_routes import payment_router
from src.routes.user_routes import user_router
from src.routes.request_routes import request_router
from src.middlewares.http_error_handler import HTTPErrorHandler
from src.configs.config import CLIENT

app = FastAPI()
app.title = 'Reservify'
app.description = "API para gestionar reservas de un restaurante en línea."
app.version = '0.0.0.1'

app.add_middleware(
    CORSMiddleware,
    allow_origins=[CLIENT],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Middleware para manejar errores HTTP
app.add_middleware(HTTPErrorHandler)

app.include_router(auth_router)
app.include_router(schedule_router)
app.include_router(table_router)
app.include_router(reservation_router)
app.include_router(payment_router)
app.include_router(user_router)
app.include_router(request_router)