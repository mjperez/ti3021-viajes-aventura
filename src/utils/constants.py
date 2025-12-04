"""Constantes del Sistema - Viajes Aventura

Centraliza todas las constantes utilizadas en el proyecto.
Facilita el mantenimiento y evita valores hardcodeados.

Uso:
    # Importar desde src.utils (recomendado):
    from src.utils import ESTADOS_RESERVA, EMAIL_MAX_LENGTH, REGEX_EMAIL
    
    # Ejemplo en validators.py:
    from src.utils import REGEX_EMAIL, EMAIL_MAX_LENGTH, MSG_ERROR_EMAIL_INVALIDO
    
    def validar_email(email: str) -> bool:
        if len(email) > EMAIL_MAX_LENGTH:
            return False
        return re.match(REGEX_EMAIL, email) is not None
    
    # Ejemplo en dao/reserva_dao.py:
    from src.utils import ESTADO_RESERVA_DEFAULT
    
    def crear(self, reserva_dto):
        reserva_dto.estado = ESTADO_RESERVA_DEFAULT
        # ...resto del código
    
    # Ejemplo en business/pago_manager.py:
    from src.utils import ESTADOS_PAGO, MSG_ERROR_ESTADO_INVALIDO
    
    if pago.estado not in ESTADOS_PAGO:
        raise ValueError(MSG_ERROR_ESTADO_INVALIDO)
"""

# ============================================
# ENUMERACIONES DE BASE DE DATOS
# ============================================
ESTADOS_RESERVA = ['PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'PAGADA']
METODOS_PAGO = ['EFECTIVO', 'TARJETA', 'TRANSFERENCIA']
ESTADOS_PAGO = ['PENDIENTE', 'COMPLETADO', 'FALLIDO']
ROLES_USUARIO = ['ADMIN', 'CLIENTE']
POLITICAS_CANCELACION = ['Flexible', 'Estricta']

# ============================================
# VALORES POR DEFECTO
# ============================================
ESTADO_RESERVA_DEFAULT = 'PENDIENTE'
ESTADO_PAGO_DEFAULT = 'PENDIENTE'
ROL_USUARIO_DEFAULT = 'CLIENTE'

# ============================================
# POLÍTICAS DE CANCELACIÓN
# ============================================
DIAS_AVISO_FLEXIBLE = 7
DIAS_AVISO_ESTRICTA = 30
REEMBOLSO_FLEXIBLE = 100  # Porcentaje
REEMBOLSO_ESTRICTA = 50   # Porcentaje

# ============================================
# VALIDACIÓN DE CAMPOS (Longitudes máximas)
# ============================================
EMAIL_MAX_LENGTH = 255
NOMBRE_MAX_LENGTH = 100
PASSWORD_MIN_LENGTH = 8
DESCRIPCION_MAX_LENGTH = 65535  # TEXT en MySQL

# ============================================
# LÍMITES DE NEGOCIO
# ============================================
MIN_PERSONAS_RESERVA = 1
MAX_PERSONAS_RESERVA = 50
MIN_CUPOS_PAQUETE = 0
MIN_DURACION_ACTIVIDAD = 1   # Horas
MAX_DURACION_ACTIVIDAD = 24  # Horas
MIN_MONTO = 0.01

# ============================================
# FORMATOS DE FECHA
# ============================================
FORMATO_FECHA_ISO = '%Y-%m-%d'
FORMATO_FECHA_CHILENO = '%d/%m/%Y'
FORMATO_DATETIME_DB = '%Y-%m-%d %H:%M:%S'
FORMATO_DATETIME_DISPLAY = '%d/%m/%Y %H:%M'

# ============================================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================================
DB_CHARSET = 'utf8mb4'
DB_PORT_DEFAULT = 3306

# ============================================
# PATRONES DE VALIDACIÓN (REGEX)
# ============================================
REGEX_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
REGEX_PASSWORD = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
REGEX_TELEFONO_CHILE = r'^(\+?56)?[2-9]\d{8}$'
REGEX_RUT = r'^\d{7,8}-[\dkK]$' # Cualesquiera 7 u 8 digitos, un guión y un digito y la letra k minuscula o mayuscula.

# ============================================
# MENSAJES DE ERROR ESTÁNDAR
# ============================================
MSG_ERROR_CUPOS = 'No hay cupos disponibles para este paquete'
MSG_ERROR_FECHA_INVALIDA = 'La fecha de fin debe ser posterior a la fecha de inicio'
MSG_ERROR_MONTO_NEGATIVO = 'El monto debe ser mayor a cero'
MSG_ERROR_EMAIL_INVALIDO = 'El formato del email no es válido'
MSG_ERROR_PASSWORD_DEBIL = 'La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número'
MSG_ERROR_PERSONAS_INVALIDO = 'El número de personas debe estar entre 1 y 50'
MSG_ERROR_ESTADO_INVALIDO = 'El estado proporcionado no es válido'
MSG_ERROR_EMAIL_DUPLICADO = 'El email ya está registrado'
MSG_ERROR_USUARIO_NO_ENCONTRADO = 'Usuario no encontrado'
MSG_ERROR_CREDENCIALES_INVALIDAS = 'Credenciales inválidas'
MSG_ERROR_PASSWORD_ACTUAL_INCORRECTA = 'Contraseña actual incorrecta'
MSG_ERROR_FECHA_FUTURA = 'La fecha debe ser futura'
MSG_ERROR_NOMBRE_INVALIDO = 'El nombre no cumple con los requisitos'
MSG_ERROR_TELEFONO_INVALIDO = 'El formato del teléfono no es válido'
MSG_ERROR_RUT_INVALIDO = 'El RUT ingresado no es válido'

# ============================================
# CONSTANTES FINANCIERAS
# ============================================
VALOR_IVA = 0.19
MONEDA_OFICIAL = "CLP"
SIMBOLO_MONEDA = "$"