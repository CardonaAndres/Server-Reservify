from src.configs.server import app
from src.configs.config import PORT

if __name__ == 'main':
    import uvicorn
    uvicorn.run(app, port = PORT)