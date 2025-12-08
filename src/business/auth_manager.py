"""Gestor de Autenticación - Business Logic

Maneja la lógica de negocio para autenticación y autorización.
Utiliza bcrypt para hashear contraseñas de forma segura.
"""

from datetime import datetime

import bcrypt

from src.dao.usuario_dao import UsuarioDAO
from src.dto.usuario_dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_CREDENCIALES_INVALIDAS,
    MSG_ERROR_EMAIL_DUPLICADO,
    MSG_ERROR_EMAIL_INVALIDO,
    MSG_ERROR_PASSWORD_ACTUAL_INCORRECTA,
    MSG_ERROR_PASSWORD_DEBIL,
    MSG_ERROR_USUARIO_NO_ENCONTRADO,
    ROL_USUARIO_DEFAULT,
    AutenticacionError,
    ValidacionError,
)
from src.utils.validators import validar_email, validar_password, validar_rut

def hashear_password(password: str) -> str:
    '''Hashea la contraseña usando bcrypt. Retorna el hash como string.'''
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    return hash_bytes.decode('utf-8')

def verificar_password(password:str,hash_pw:str) -> bool:
    '''Verifica si la contraseña coincide con el hash almacenado. Retorna True si coincide.''' 
    return bcrypt.checkpw(password.encode('utf-8'),hash_pw.encode('utf-8'))

def registrar_usuario(rut, email, password, nombre, rol=None) -> UsuarioDTO:
    '''Registra un nuevo usuario tras validar rut, email y password. Retorna el DTO del usuario creado.'''
    if not validar_rut(rut):
        raise ValidacionError("RUT inválido")

    if not validar_email(email):
        raise ValidacionError(MSG_ERROR_EMAIL_INVALIDO)
    
    if not validar_password(password):
        raise ValidacionError(MSG_ERROR_PASSWORD_DEBIL)
    dao = UsuarioDAO()
    
    # Validar unicidad
    usuarioExistenteEmail = dao.obtener_por_email(email)
    if usuarioExistenteEmail:
        raise ValidacionError(MSG_ERROR_EMAIL_DUPLICADO)

    # Validar unicidad (RUT debe ser único)
    usuarioExistenteRut = dao.obtener_por_rut(rut)
    if usuarioExistenteRut:
        raise ValidacionError("RUT duplicado")
    
    hashpw = hashear_password(password)
    usuarioNuevo = UsuarioDTO(None, rut, email, hashpw, nombre, rol or ROL_USUARIO_DEFAULT, datetime.now())
    idNuevo = dao.crear(usuarioNuevo)
    usuarioNuevo.id = idNuevo
    return usuarioNuevo

def login(email:str,passw:str) -> UsuarioDTO|None:
    '''Login de usuario, retorna DTO si es válido'''
    dao = UsuarioDAO()
    try:
        usuario = dao.obtener_por_email(email)
    except Exception:
        raise AutenticacionError(MSG_ERROR_CREDENCIALES_INVALIDAS)
    
    if usuario and verificar_password(passw,usuario.password_hash):    
        return usuario
    raise AutenticacionError(MSG_ERROR_CREDENCIALES_INVALIDAS)

def cambiar_password(usuarioID: int, passwordActual: str, passwordNueva: str) -> bool:
    '''Cambia la contraseña del usuario tras validar la actual. Retorna True si se actualizó.'''
    dao = UsuarioDAO()
    try:
        usuario = dao.obtener_por_id(usuarioID)
    except Exception:
        raise AutenticacionError(MSG_ERROR_USUARIO_NO_ENCONTRADO)
    
    if not usuario:
        raise ValidacionError(MSG_ERROR_USUARIO_NO_ENCONTRADO)

    if not verificar_password(passwordActual, usuario.password_hash):
        raise AutenticacionError(MSG_ERROR_PASSWORD_ACTUAL_INCORRECTA)
    
    if not validar_password(passwordNueva):
        raise ValidacionError(MSG_ERROR_PASSWORD_DEBIL)

    usuario.password_hash = hashear_password(passwordNueva)
    return dao.actualizar(usuario)