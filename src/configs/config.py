
SECRET_KEY = "clave_secreta_1234" 
ALGORITHM = "HS256" # Algoritmo de encriptación para el JWT

PORT = 8000

is_production = False

CLIENT = 'http://localhost:5173'

db_config = {
    'host' : 'localhost', #dokcer(host.docker.internal) |trabajo en local(localhost)
    'user' : 'root',
    'password' : '',
    'db' : 'reservify_db',
    'port' : 3306,
    'loop': None
}