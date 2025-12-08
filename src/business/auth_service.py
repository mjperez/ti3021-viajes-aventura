from datetime import datetime
import bcrypt
from src.dao.usuario_dao import UsuarioDAO
from src.dto.usuario_dto import UsuarioDTO
from src.utils.exceptions import AutenticacionError, ValidacionError
from src.utils.constants import (
    MSG_ERROR_CREDENCIALES_INVALIDAS,
    MSG_ERROR_EMAIL_DUPLICADO,
    MSG_ERROR_EMAIL_INVALIDO,
    MSG_ERROR_PASSWORD_ACTUAL_INCORRECTA,
    MSG_ERROR_PASSWORD_DEBIL,
    MSG_ERROR_USUARIO_NO_ENCONTRADO,
    ROL_USUARIO_DEFAULT,
)
from src.utils.validators import validar_email, validar_password, validar_rut

class AuthService:
    """Servicio de Autenticación.
    
    Encapsula la lógica de registro, login y gestión de credenciales.
    """
    
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def _hashear_password(self, password: str) -> str:
        """Hashea la contraseña usando bcrypt. Método privado/interno."""
        hash_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hash_bytes.decode('utf-8')

    def _verificar_password(self, password: str, hash_pw: str) -> bool:
        """Verifica la contraseña. Método privado/interno."""
        return bcrypt.checkpw(password.encode('utf-8'), hash_pw.encode('utf-8'))

    def registrar_usuario(self, rut: str, email: str, password: str, nombre: str, rol: str = None) -> UsuarioDTO:
        """Registra un nuevo usuario tras validar rut, email y password."""
        if not validar_rut(rut):
            raise ValidacionError("RUT inválido")

        if not validar_email(email):
            raise ValidacionError(MSG_ERROR_EMAIL_INVALIDO)
        
        if not validar_password(password):
            raise ValidacionError(MSG_ERROR_PASSWORD_DEBIL)
        
        # Validar unicidad de Email
        if self.usuario_dao.obtener_por_email(email):
            raise ValidacionError(MSG_ERROR_EMAIL_DUPLICADO)

        # Validar unicidad de RUT
        if self.usuario_dao.obtener_por_rut(rut):
            raise ValidacionError("RUT duplicado")
        
        hashpw = self._hashear_password(password)
        usuario_nuevo = UsuarioDTO(None, rut, email, hashpw, nombre, rol or ROL_USUARIO_DEFAULT, datetime.now())
        
        id_nuevo = self.usuario_dao.crear(usuario_nuevo)
        usuario_nuevo.id = id_nuevo
        return usuario_nuevo

    def login(self, email: str, passw: str) -> UsuarioDTO:
        """Inicia sesión validando credenciales."""
        try:
            usuario = self.usuario_dao.obtener_por_email(email)
        except Exception:
            raise AutenticacionError(MSG_ERROR_CREDENCIALES_INVALIDAS)
        
        if usuario and self._verificar_password(passw, usuario.password_hash):    
            return usuario
        raise AutenticacionError(MSG_ERROR_CREDENCIALES_INVALIDAS)

    def cambiar_password(self, usuario_id: int, password_actual: str, password_nueva: str) -> bool:
        """Cambia la contraseña del usuario."""
        try:
            usuario = self.usuario_dao.obtener_por_id(usuario_id)
        except Exception:
            raise AutenticacionError(MSG_ERROR_USUARIO_NO_ENCONTRADO)
        
        if not usuario:
            raise ValidacionError(MSG_ERROR_USUARIO_NO_ENCONTRADO)

        if not self._verificar_password(password_actual, usuario.password_hash):
            raise AutenticacionError(MSG_ERROR_PASSWORD_ACTUAL_INCORRECTA)
        
        if not validar_password(password_nueva):
            raise ValidacionError(MSG_ERROR_PASSWORD_DEBIL)

        usuario.password_hash = self._hashear_password(password_nueva)
        return self.usuario_dao.actualizar(usuario)
