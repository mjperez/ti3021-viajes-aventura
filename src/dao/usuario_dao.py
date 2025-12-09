from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.usuario_dto import UsuarioDTO


class UsuarioDAO:
    #Maneja todas las operaciones de base de datos relacionadas con Usuarios.
    def __init__(self):
        pass
    
    def crear(self, usuario_dto: UsuarioDTO) -> int:
        """Inserta un nuevo usuario. Retorna ID del usuario creado"""
        sql = "INSERT INTO Usuarios (rut, email, password_hash, nombre, rol, fecha_registro) VALUES (%s,%s,%s,%s,%s,%s)"

        params = (
            usuario_dto.rut,
            usuario_dto.email,
            usuario_dto.password_hash,usuario_dto.nombre,
            usuario_dto.rol,
            usuario_dto.fecha_registro
            )

        return ejecutar_insercion(sql,params)
    
    def obtener_por_id(self, id: int) -> UsuarioDTO | None:
        """Busca usuario por ID. Retorna UsuarioDTO o None"""
        sql = "SELECT * FROM Usuarios WHERE id=%s"
        params=(id,)

        usuario = ejecutar_consulta_uno(sql, params)

        if usuario:
            return UsuarioDTO(
                id=usuario['id'],
                rut=usuario['rut'],
                email=usuario['email'],
                password_hash=usuario['password_hash'],
                nombre=usuario['nombre'],
                rol=usuario['rol'],
                fecha_registro=usuario['fecha_registro']
            )

        return None
    
    def obtener_por_rut(self, rut: str) -> UsuarioDTO | None:
        """Busca usuario por RUT. Retorna UsuarioDTO o None"""
        sql = "SELECT * FROM Usuarios WHERE rut=%s"
        params=(rut,)

        usuario = ejecutar_consulta_uno(sql, params)

        if usuario:
            return UsuarioDTO(
                id=usuario['id'],
                rut=usuario['rut'],
                email=usuario['email'],
                password_hash=usuario['password_hash'],
                nombre=usuario['nombre'],
                rol=usuario['rol'],
                fecha_registro=usuario['fecha_registro']
            )
        return None
    
    def obtener_por_email(self, email: str) -> UsuarioDTO | None:
        """Busca usuario por email. Retorna UsuarioDTO o None"""
        sql = "SELECT * FROM Usuarios WHERE email=%s"
        params=(email,)

        usuario = ejecutar_consulta_uno(sql, params)

        if usuario:
            return UsuarioDTO(
                id=usuario['id'],
                rut=usuario['rut'],
                email=usuario['email'],
                password_hash=usuario['password_hash'],
                nombre=usuario['nombre'],
                rol=usuario['rol'],
                fecha_registro=usuario['fecha_registro']
            )
        return None
    
    def listar_todos(self) -> list[UsuarioDTO]:
        """Lista todos los usuarios (admin). Retorna Lista de UsuarioDTO"""
        sql = "SELECT * FROM Usuarios"
        rows = ejecutar_consulta(sql)
        usuarios = []
        
        if not rows:
            return []
        
        for r in rows:
            usuarios.append(
                UsuarioDTO(
                    id=r['id'],
                    rut=r['rut'],
                    email=r['email'],
                    password_hash=r['password_hash'],
                    nombre=r['nombre'],
                    rol=r['rol'],
                    fecha_registro=r['fecha_registro']
                )
            )

        return usuarios
    
    def actualizar(self, usuario_dto: UsuarioDTO) -> bool:
        """Actualiza datos del usuario. Retorna True si se actualizó"""
        sql = "UPDATE Usuarios SET rut = %s, email = %s, password_hash = %s, nombre = %s, rol = %s, fecha_registro = %s WHERE id = %s"
        params= (usuario_dto.rut, usuario_dto.email, usuario_dto.password_hash, usuario_dto.nombre, usuario_dto.rol, usuario_dto.fecha_registro, usuario_dto.id)

        filas = ejecutar_actualizacion(sql,params)
        return filas > 0

    
    def eliminar(self, id: int) -> bool:
        """Elimina un usuario. Retorna True si se eliminó"""
        sql = "DELETE FROM Usuarios WHERE id = %s"
        params = (id,)

        filas = ejecutar_actualizacion(sql,params)
        return filas > 0

    def listar_por_rol(self, rol:str) -> list[UsuarioDTO]: 
        """Lista usuarios por rol. Retorna Lista de UsuarioDTO"""
        sql = "SELECT * FROM Usuarios WHERE rol = %s"
        params = (rol,)
        usuarios = []
        rows = ejecutar_consulta(sql,params)                
        
        if not rows:
            return []
        
        for r in rows:
            usuarios.append(UsuarioDTO(
                id=r['id'],
                rut=r['rut'],
                email=r['email'],
                password_hash=r['password_hash'],
                nombre=r['nombre'],
                rol=r['rol'],
                fecha_registro=r['fecha_registro']
            ))

        return usuarios

    def verificar_email_existe(self, email:str) -> bool: 
        """Valida si el email ya está registrado. Retorna True si existe"""
        sql = "SELECT * FROM Usuarios WHERE email = %s"
        params = (email,)

        usuario = ejecutar_consulta_uno(sql,params)

        if not usuario:
            return False
        return True
