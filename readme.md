## Server-Reservify

**Server-Reservify** es una API desarrollada con FastAPI para gestionar reservas en línea de un restaurante. Utiliza MySQL como base de datos, administrada a través de phpMyAdmin, y maneja las consultas SQL directamente sin emplear un ORM.

## Características

- **Gestión de reservas de mesas**: Permite a los clientes reservar mesas y gestionarlas, y al administrador permite llevar un controlor o registro de estas.
- **Gestión de Horarios**: Administra los horarios de apertura y disponibilidad de mesas.
- **Historial de Reservas**: Mantiene un registro de todas las reservas realizadas.
- **Gestión de usuarios**: Administra la creación y gestión de usuarios y sus roles dentro del sistema.
- **Gestión de de solicitudes de los usuarios**: Permite a los usuarios enviar peticiones o mensajes a los administradores.

## Requisitos Previos

- **Python 3.8+**: Asegúrate de tener Python instalado. 
- **MySQL**: Instala MySQL y phpMyAdmin para la gestión de la base de datos.
- **FastAPI**: Se recomienda instalar FastAPI y Uvicorn para el servidor ASGI.

## Instalación

1. **Clona el repositorio**:
    ```bash
    git clone https://github.com/CardonaAndres/Server-Reservify.git
    cd Server-Reservify
    ```

2. **Crea y activa un entorno virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. **Instala las dependencias**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configura la base de datos**:
    - Crea una base de datos en MySQL para la aplicación.
    - Importa el esquema de base de datos utilizando phpMyAdmin o la línea de comandos de MySQL.
    - Actualiza las credenciales de la base de datos en el archivo de configuración de la aplicación.

5. **Ejecuta la aplicación**:
    ```bash
    uvicorn src.main:app --reload
    ```

    La API estará disponible en `http://127.0.0.1:8000`.

## Uso

- **Documentación Interactiva**: Accede a `http://127.0.0.1:8000/docs` para explorar y probar los endpoints de la API utilizando la interfaz de Swagger.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## Ejecución con Docker

Para facilitar la implementación y ejecución de **Server-Reservify**, el proyecto está configurado para ejecutarse en contenedores Docker. 

**Desarrollado por [Andrés Cardona](https://github.com/CardonaAndres)**