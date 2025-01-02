# Usa una imagen base oficial de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos desde la carpeta src
COPY src/requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la carpeta src al contenedor
COPY src /app/src

# Exponer el puerto que FastAPI usará
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
