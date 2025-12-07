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
        # INSERT y retornar lastrowid
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
        # SELECT por ID
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
    
    def obtener_por_email(self, email: str) -> UsuarioDTO | None:
        # SELECT por email (para login)
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
        # SELECT * y retornar lista de DTOs
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
        # UPDATE y retornar True si tuvo éxito
        sql = "UPDATE Usuarios SET rut = %s, email = %s, password_hash = %s, nombre = %s, rol = %s, fecha_registro = %s WHERE id = %s"
        params= (usuario_dto.rut, usuario_dto.email, usuario_dto.password_hash, usuario_dto.nombre, usuario_dto.rol, usuario_dto.fecha_registro, usuario_dto.id)

        filas = ejecutar_actualizacion(sql,params)
        return filas > 0

    
    def eliminar(self, id: int) -> bool:
        # DELETE y retornar True si tuvo éxito
        sql = "DELETE FROM Usuarios WHERE id = %s"
        params = (id,)

        filas = ejecutar_actualizacion(sql,params)
        return filas > 0

    def listar_por_rol(self, rol:str) -> list[UsuarioDTO]: 
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
        #Valida si el email ya está registrado
        sql = "SELECT * FROM Usuarios WHERE email = %s"
        params = (email,)

        usuario = ejecutar_consulta_uno(sql,params)

        if not usuario:
            return False
        return True
