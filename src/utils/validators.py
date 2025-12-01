"""Validadores - Utilidades de Validación

Funciones para validar datos de entrada del usuario.
Asegura la integridad de datos antes de procesarlos.

Funciones esperadas:
    - validar_email(email): Valida formato de email con regex
    - validar_password(password): Valida requisitos de contraseña segura
    - validar_numero_positivo(numero): Valida que sea número positivo
    - validar_fecha(fecha_str): Valida formato de fecha
    - validar_fecha_futura(fecha): Valida que la fecha sea futura
    - validar_rango_fechas(fecha_inicio, fecha_fin): Valida rango válido
    - validar_telefono(telefono): Valida formato de teléfono
    - validar_enum(valor, opciones): Valida que el valor esté en lista permitida
    - sanitizar_input(texto): Limpia entrada de caracteres peligrosos

Criterios de validación:
    - Email: formato estándar (usuario@dominio.com)
    - Password: mínimo 8 caracteres, mayúscula, minúscula, número
    - Fechas: formato YYYY-MM-DD o DD/MM/YYYY
"""

# validators.py

# Constantes para ENUM
ESTADOS_RESERVA = ['PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'PAGADA']
METODOS_PAGO = ['EFECTIVO', 'TARJETA', 'TRANSFERENCIA']
ESTADOS_PAGO = ['PENDIENTE', 'COMPLETADO', 'FALLIDO']
ROLES_USUARIO = ['ADMIN', 'CLIENTE']

def validar_estado_reserva(estado: str) -> bool:
    """Valida que el estado de reserva sea válido"""
    if not estado:
        return False
    return estado.upper() in ESTADOS_RESERVA