
SECRET_KEY = "clave_secreta_1234" 
ALGORITHM = "HS256" # Algoritmo de encriptación para el JWT

PORT = 8000

is_production = False

CLIENT = ''

db_config = {
    'host' : 'host.docker.internal',
    'user' : 'root',
    'password' : '',
    'db' : 'reservify_db',
    'port' : 3306,
    'loop': None
}