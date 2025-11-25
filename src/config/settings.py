"""Configuración del Sistema - Settings

Centraliza todas las configuraciones de la aplicación.
Carga variables de entorno desde archivo .env

Configuraciones esperadas:

# Database
DB_HOST: Host de MySQL (default: localhost)
DB_PORT: Puerto de MySQL (default: 3306)
DB_NAME: Nombre de la base de datos (default: viajes_aventura)
DB_USER: Usuario de MySQL
DB_PASSWORD: Contraseña de MySQL

# Security
SECRET_KEY: Clave secreta para encriptación
BCRYPT_ROUNDS: Rondas de bcrypt (default: 12)

# Application
APP_NAME: Nombre de la aplicación
DEBUG: Modo debug (default: False)
LOG_LEVEL: Nivel de logging (default: INFO)

# Business Rules
MIN_PASSWORD_LENGTH: Longitud mínima de contraseña (default: 8)
MAX_PERSONAS_POR_RESERVA: Máximo de personas por reserva (default: 10)

Uso:
    from src.config.settings import DB_HOST, DB_PORT

Requiere:
    - python-dotenv para cargar archivo .env
"""