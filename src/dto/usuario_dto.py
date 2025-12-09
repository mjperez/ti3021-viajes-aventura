from dataclasses import dataclass
from datetime import datetime


@dataclass
class UsuarioDTO:
    """Transfer Object para Usuario. Representa los datos de un usuario del sistema."""
    id: int | None
    rut: str
    email: str
    password_hash: str
    nombre: str
    rol: str
    fecha_registro: datetime
    
    def __repr__(self):
        return (f"UsuarioDTO(id={self.id}, rut='{self.rut}', nombre='{self.nombre}', email='{self.email}', rol='{self.rol}')")