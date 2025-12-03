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

import bcrypt
from dao.usuario_dao import UsuarioDAO
import utils.validators