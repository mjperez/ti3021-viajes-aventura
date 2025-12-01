"""DTO para Usuario - Data Transfer Object

Clase que representa los datos de un usuario del sistema.
Utilizada para transferir información entre capas sin lógica de negocio.

Atributos esperados:
    - id: int
    - email: string
    - password_hash: string
    - nombre: string
    - rol: string ('cliente' o 'administrador')
    - fecha_registro: datetime
"""
from datetime import datetime


class UsuarioDTO():
    
    def __init__(self,id_usuario: int, email:str, pass_hash: str, rol: str, fecha_registro: datetime):
        self.id_usuario = id_usuario
        self.email = email
        self.pass_hash = pass_hash
        self.rol = rol
        self.fecha_registro = fecha_registro