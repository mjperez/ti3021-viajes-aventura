"""
Funciones para validar datos de entrada del usuario. Asegura la integridad de datos antes de procesarlos.
Criterios de validación:
    - Email: formato estándar (usuario@dominio.com)
    - Password: mínimo 8 caracteres, mayúscula, minúscula, número
    - Fechas: formato YYYY-MM-DD o DD/MM/YYYY
"""

import re  # librería expresiones regulares
from datetime import datetime
from itertools import cycle  # crea una lista infinita que se repite.

from src.utils import (
    EMAIL_MAX_LENGTH,
    ESTADOS_PAGO,
    ESTADOS_RESERVA,
    FORMATO_FECHA_CHILENO,
    FORMATO_FECHA_ISO,
    MAX_PERSONAS_RESERVA,
    METODOS_PAGO,
    MIN_MONTO,
    MIN_PERSONAS_RESERVA,
    PASSWORD_MIN_LENGTH,
    REGEX_EMAIL,
    REGEX_PASSWORD,
    REGEX_RUT,
    REGEX_TELEFONO_CHILE,
    ROLES_USUARIO,
)


def validar_estado_reserva(estado: str) -> bool:
    """Valida que el estado de reserva sea válido"""
    if not estado:
        return False
    return estado.upper() in ESTADOS_RESERVA

def validar_rut(rut: str) -> bool:
    #Valida que el rut cumpla el formato esperado y la matemática de verificación
    rut = rut.replace('.','').strip().upper() # se limpia rut si tiene puntos

    if not re.match(REGEX_RUT,rut): # si el rut no tiene el formato correcto, no valida rut
        return False
    
    try:
        cuerpo, dv = rut.split('-') #intenta separar el cuerpo y el digito verificador
    except ValueError: # si por alguna razon el string paso el regex sin que el guión existiera, esto lo detiene.
        return False
    
    # Cálculo matematico del digito verificador
    #Para validar el RUT, hay que multiplicar los números de derecha a izquierda por una serie que es 2, 3, 4, 5, 6, 7. Luego hay que sumar los multiplos y calcular el resto cuando se divide la suma en 11. Dependiendo del valor de 11 - resto, se puede saber que digito verificador se espera de ese rut en particular.

    reverso = map(int, reversed(cuerpo)) # reversed devuelve un iterador reverso, map(int) convierte los numeros del iterador de str a int
    factores = cycle(range(2,8)) # crea lista entre el 2 y el 7

    suma = sum(d * f for d,f in zip(reverso,factores)) #zip es un iterador de tuplas, toma el primer digito del rut y el primer digito de la lista de factores y los junta. luego, d*f los multiplica y finalmente todas las parejas de multiplicación se suman.
    
    resto = suma % 11 # se obtiene el resto con modulo
    dvCalculado = 11 - resto # se calcula el digito verificador

    if dvCalculado == 11: # si el digito verificador calculado es 11, el digito verificador esperado es 0
        dvEsperado = 0
    elif dvCalculado == 10: # en cambio si es 10, el digito verificador esperado es la letra K
        dvEsperado = 'K'
    else: # si no es 'K' ni 0, es el número calculado en la resta de 11 - resto.
        dvEsperado = str(dvCalculado)
    
    return dvEsperado == dv # si el digito verificador esperado es igual al digito verificador entregado por el usuario, retorna True. en caso contrario, False

def validar_email(email: str) -> bool:
    #Valida formato de email con regex
    if not email or len(email) > EMAIL_MAX_LENGTH:
        return False
    return re.match(REGEX_EMAIL, email) is not None

def validar_password(password: str) -> bool:
    #Valida requisitos de contraseña segura
    if not password or len(password) < PASSWORD_MIN_LENGTH: # si password es vacio o de menor largo que el requerido, retorna falso
        return False
    return re.match(REGEX_PASSWORD,password) is not None # match devuelve none si no hay match en la comparacion.

def validar_numero_positivo(numero: float) -> bool:
    #Valida que sea número positivo
    try:
        return float(numero) > 0
    except (ValueError,TypeError):
        return False

def validar_monto(monto:float) -> bool:
    try:
        return float(monto) >= MIN_MONTO
    except (ValueError,TypeError):
        return False
    
def validar_fecha(fecha_str:str, formato:str = "") -> bool:
    #Valida formato de fecha
    if not fecha_str:
        return False
    formatos = [formato] if formato else [FORMATO_FECHA_ISO,FORMATO_FECHA_CHILENO]

    for f in formatos:
        try:
            datetime.strptime(fecha_str,f) # intenta validar formato ISO y luego chileno
            return True
        except ValueError: # si hay valueerror, sigue el ciclo for
            continue
    return False # si llega hasta aqui no tiene el formato valido.

def validar_fecha_futura(fecha:datetime)-> bool:
    #Valida que la fecha sea futura
    return fecha > datetime.now()

def validar_rango_fechas(fecha_inicio:datetime,fecha_fin:datetime)-> bool:
    return fecha_fin > fecha_inicio

def validar_telefono(telefono:str) -> bool:
    if not telefono:
        return False
    return re.match(REGEX_TELEFONO_CHILE,telefono) is not None

def validar_enum(valor:str,opciones:list) -> bool:
    #valida que valor este en la lista de opciones
    if not valor or not opciones:
        return False
    return valor.upper() in [str(opc).upper() for opc in opciones]

def validar_estado_pago(estado:str)->bool:
    return validar_enum(estado,ESTADOS_PAGO)

def validar_metodo_pago(metodo:str)->bool:
    return validar_enum(metodo,METODOS_PAGO)

def validar_rol_usuario(rol:str)->bool:
    return validar_enum(rol,ROLES_USUARIO)

def validar_numero_personas(numero:int)-> bool:
    try:
        n = int(numero)
        return MIN_PERSONAS_RESERVA <= n <= MAX_PERSONAS_RESERVA
    except (ValueError,TypeError):
        return False

def validar_dias_aviso(dias: int) -> bool:
    """Valida que los días de aviso sean válidos (0-365)."""
    try:
        d = int(dias)
        return 0 <= d <= 365
    except (ValueError, TypeError):
        return False

def validar_porcentaje_reembolso(porcentaje: float) -> bool:
    """Valida que el porcentaje de reembolso esté entre 0 y 100."""
    try:
        p = float(porcentaje)
        return 0 <= p <= 100
    except (ValueError, TypeError):
        return False

def sanitizar_input(texto:str) -> str:
    #Limpia input de caracteres peligrosos para evitar SQL injection
    if not texto:
        return ""
    return texto.strip().replace("'","").replace('"',"").replace(';','').replace('--','')
