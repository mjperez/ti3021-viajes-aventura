"""Service Layer para Usuarios

Encapsula la lógica de negocio relacionada con usuarios.
Intermediario entre la UI y el DAO para mantener separación de capas.
"""

from src.dao.usuario_dao import UsuarioDAO
from src.dto.usuario_dto import UsuarioDTO
from src.utils.exceptions import ValidacionError


class UsuarioService:
    """Servicio para gestión de usuarios."""
    
    def __init__(self):
        """Inicializa el servicio con su DAO."""
        self.usuario_dao = UsuarioDAO()
    
    def obtener_usuario(self, usuario_id: int) -> UsuarioDTO | None:
        """Obtiene un usuario por ID. Retorna UsuarioDTO o None si no existe"""
        if usuario_id <= 0:
            raise ValidacionError("El ID del usuario debe ser mayor a 0")
        
        return self.usuario_dao.obtener_por_id(usuario_id)
    
    def obtener_usuario_por_email(self, email: str) -> UsuarioDTO | None:
        """Obtiene un usuario por email. Retorna UsuarioDTO o None si no existe"""
        if not email or not email.strip():
            raise ValidacionError("El email no puede estar vacío")
        
        return self.usuario_dao.obtener_por_email(email.strip())
    
    def actualizar_perfil(
        self,
        usuario_id: int,
        nombre: str
    ) -> UsuarioDTO:
        """Actualiza el perfil de un usuario. Retorna UsuarioDTO actualizado"""
        # Validaciones
        if usuario_id <= 0:
            raise ValidacionError("El ID del usuario debe ser mayor a 0")
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre no puede estar vacío")
        
        # Verificar existencia
        usuario_existente = self.usuario_dao.obtener_por_id(usuario_id)
        if not usuario_existente:
            raise ValidacionError(f"No existe un usuario con ID {usuario_id}")
        
        # Actualizar
        usuario_existente.nombre = nombre.strip()
        
        success = self.usuario_dao.actualizar(usuario_existente)
        if not success:
            raise ValidacionError(f"No se pudo actualizar el usuario con ID {usuario_id}")
        
        return usuario_existente
    
    def listar_todos_usuarios(self) -> list[UsuarioDTO]:
        """Lista todos los usuarios. Retorna Lista de UsuarioDTO"""
        return self.usuario_dao.listar_todos()
