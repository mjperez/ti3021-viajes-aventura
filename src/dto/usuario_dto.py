from datetime import datetime


class UsuarioDTO():
    # Clase que representa los datos de un usuario del sistema.
    def __init__(self,id: int | None, email:str, password_hash: str, nombre:str, rol: str, fecha_registro: datetime):
        self.id = id
        self.email = email
        self.password_hash = password_hash
        self.nombre=nombre
        self.rol = rol
        self.fecha_registro = fecha_registro
    
    def __repr__(self):
        return (f"UsuarioDTO(id={self.id},nombre='{self.nombre}', email='{self.email}', rol='{self.rol}')")