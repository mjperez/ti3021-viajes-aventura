"""Gestor de Autenticación - Business Logic

Maneja la lógica de negocio para autenticación y autorización.
Utiliza bcrypt para hashear contraseñas de forma segura.

Funciones esperadas:
    - registrar_usuario(email, password, nombre, rol): Registra nuevo usuario con hash
    - login(email, password): Autentica usuario y retorna DTO si es válido
    - hashear_password(password): Genera hash bcrypt de la contraseña
    - verificar_password(password, hash): Verifica contraseña contra hash
    - cambiar_password(usuario_id, password_actual, password_nueva): Cambia contraseña
    - validar_email(email): Valida formato de email
    - validar_password_segura(password): Valida requisitos de seguridad
    - obtener_usuario_actual(): Retorna el usuario autenticado en sesión

Requiere:
    - bcrypt para hashing
    - usuario_dao para acceso a datos
    - validators para validaciones
"""

import re
from datetime import datetime

import bcrypt

from src.dao.usuario_dao import UsuarioDAO
from src.dto.usuario_dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_EMAIL_INVALIDO,
    MSG_ERROR_PASSWORD_DEBIL,
    REGEX_EMAIL,
    REGEX_PASSWORD,
    ROL_USUARIO_DEFAULT,
    AutenticacionError,
    ValidacionError,
)


def hashear_password(password: str) -> str:
    hash_bytes = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    return hash_bytes.decode('utf-8')

def verificar_password(password:str,hash_pw:str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'),hash_pw.encode('utf-8'))

def validar_email(email:str) -> bool:
    return re.match(REGEX_EMAIL,email) is not None

def validar_pw_segura(password:str) -> bool:
    return re.match(REGEX_PASSWORD,password) is not None

def registrar_usuario(email,password,nombre,rol=None) -> UsuarioDTO:
    if not validar_email(email):
        raise ValidacionError(MSG_ERROR_EMAIL_INVALIDO)
    
    if not validar_pw_segura(password):
        raise ValidacionError(MSG_ERROR_PASSWORD_DEBIL)
    dao = UsuarioDAO()
    usuarioExistente = dao.obtener_por_email(email)
    if usuarioExistente:
        raise ValidacionError("El email ya está registrado")
    
    hashpw = hashear_password(password)
    usuarioNuevo = UsuarioDTO(None,email,hashpw,nombre,rol or ROL_USUARIO_DEFAULT,datetime.now())
    idNuevo = dao.crear(usuarioNuevo)
    usuarioNuevo.id = idNuevo
    return usuarioNuevo

def login(email:str,passw:str) -> UsuarioDTO|None:
    dao = UsuarioDAO()
    try:
        usuario = dao.obtener_por_email(email)
    except Exception:
        raise AutenticacionError("Credenciales inválidas")
    
    if usuario and verificar_password(passw,usuario.password_hash):    
        return usuario
    raise AutenticacionError("Credenciales inválidas")

def cambiar_password(usuarioID: int, passwordActual: str, passwordNueva: str) -> bool:
    dao = UsuarioDAO()
    try:
        usuario = dao.obtener_por_id(usuarioID)
    except Exception:
        raise AutenticacionError("Usuario no Encontrado")
    
    if not usuario:
        raise ValidacionError("Usuario no encontrado")

    if not verificar_password(passwordActual, usuario.password_hash):
        raise AutenticacionError("Contraseña actual incorrecta")
    
    if not validar_pw_segura(passwordNueva):
        raise ValidacionError(MSG_ERROR_PASSWORD_DEBIL)

    usuario.password_hash = hashear_password(passwordNueva)
    return dao.actualizar(usuario)