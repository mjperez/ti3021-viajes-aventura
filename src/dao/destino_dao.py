from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.destino_dto import DestinoDTO

"""CREATE TABLE Destinos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    costo_base DECIMAL(10,2) NOT NULL,
    INDEX idx_nombre (nombre)
) ENGINE=InnoDB;"""

class DestinoDAO():
    # Maneja todas las operaciones de base de datos relacionadas con Destinos.

    def crear(self, destino_dto: DestinoDTO) -> int: 
        #Inserta un nuevo destino
        sql = "INSERT INTO Destinos (id, nombre, descripcion, costo_base) VALUES (%s,%s,%s,%s)"
        params=(destino_dto.id,destino_dto.nombre,destino_dto.descripcion,destino_dto.costo_base)
        return ejecutar_insercion(sql,params)
        
    def obtener_por_id(self, id: int) -> DestinoDTO | None: 
        #Busca destino por ID
        sql = "SELECT * FROM Destinos WHERE id = %s"
        params= (id,)
        destino = ejecutar_consulta_uno(sql,params)
        if not destino:
            return None
        return DestinoDTO(
            id = destino['id'],
            nombre = destino['nombre'],
            descripcion= destino['descripcion'],
            costo_base= destino['costo_base']
            )
        
        ...
    def actualizar(self, id: int, destino_dto: DestinoDTO) -> bool: 
        #Actualiza datos del destino
        sql = "UPDATE Destinos SET nombre=%s, descripcion=%s, costo_base=%s WHERE id=%s"
        params = (destino_dto.nombre, destino_dto.descripcion, destino_dto.costo_base, id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def eliminar(self, id: int) -> bool: 
        #Elimina un destino
        sql = "DELETE FROM Destinos WHERE id=%s"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def listar_todos(self) -> list[DestinoDTO]: 
        #Retorna lista de todos los destinos
        sql = "SELECT * FROM Destinos"
        destinos = ejecutar_consulta(sql)
        
        if not destinos:
            return []
        
        return [
            DestinoDTO(
                id=d['id'],
                nombre=d['nombre'],
                descripcion=d['descripcion'],
                costo_base=d['costo_base']
            )
            for d in destinos
        ]
    
    def buscar_por_nombre(self, nombre: str) -> list[DestinoDTO]:
        #Busca destinos por nombre (LIKE)
        sql = "SELECT * FROM Destinos WHERE nombre LIKE %s"
        params = (f"%{nombre}%",)
        destinos = ejecutar_consulta(sql, params)
        
        if not destinos:
            return []
        
        return [
            DestinoDTO(
                id=d['id'],
                nombre=d['nombre'],
                descripcion=d['descripcion'],
                costo_base=d['costo_base']
            )
            for d in destinos
        ]