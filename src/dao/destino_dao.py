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
        sql = "INSERT INTO Destinos (nombre, descripcion, costo_base, cupos_disponibles, politica_id) VALUES (%s, %s, %s, %s, %s)"
        params=(destino_dto.nombre,destino_dto.descripcion,destino_dto.costo_base,destino_dto.cupos_disponibles,destino_dto.politica_id)
        return ejecutar_insercion(sql,params)
        
    def obtener_por_id(self, id: int) -> DestinoDTO | None:
        """Busca destino activo por ID."""
        sql = "SELECT * FROM Destinos WHERE id = %s AND activo = 1"
        params = (id,)
        destino = ejecutar_consulta_uno(sql, params)
        if not destino:
            return None
        return DestinoDTO(
            id = destino['id'],
            nombre = destino['nombre'],
            descripcion= destino['descripcion'],
            costo_base= destino['costo_base'],
            cupos_disponibles= destino['cupos_disponibles'],
            politica_id= destino.get('politica_id', 1)
            )
        
        ...
    def actualizar(self, id: int, destino_dto: DestinoDTO) -> bool: 
        #Actualiza datos del destino
        sql = "UPDATE Destinos SET nombre=%s, descripcion=%s, costo_base=%s, cupos_disponibles=%s, politica_id=%s WHERE id=%s"
        params = (destino_dto.nombre, destino_dto.descripcion, destino_dto.costo_base, destino_dto.cupos_disponibles, destino_dto.politica_id, id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def eliminar(self, id: int) -> bool:
        """Elimina un destino con lógica híbrida:
        - Si tiene paquetes asociados: borrado lógico (activo=FALSE)
        - Si NO tiene paquetes: borrado físico (DELETE)
        """
        # Verificar si el destino está en uso en Paquete_Destino
        sql_check = "SELECT COUNT(*) as count FROM Paquete_Destino WHERE destino_id=%s"
        params_check = (id,)
        resultado = ejecutar_consulta_uno(sql_check, params_check)
        
        en_uso = resultado['count'] > 0 if resultado else False
        
        if en_uso:
            # Borrado lógico: desactivar el destino
            sql = "UPDATE Destinos SET activo = FALSE WHERE id=%s"
            params = (id,)
            filas = ejecutar_actualizacion(sql, params)
            return filas > 0
        else:
            # Borrado físico: eliminar completamente
            sql = "DELETE FROM Destinos WHERE id=%s"
            params = (id,)
            filas = ejecutar_actualizacion(sql, params)
            return filas > 0
    
    def listar_todos(self) -> list[DestinoDTO]:
        """Retorna lista de todos los destinos activos."""
        sql = "SELECT * FROM Destinos WHERE activo = 1 ORDER BY id ASC"
        destinos = ejecutar_consulta(sql)        
        if not destinos:
            return []
        
        return [
            DestinoDTO(
                id=d['id'],
                nombre=d['nombre'],
                descripcion=d['descripcion'],
                costo_base=d['costo_base'],
                cupos_disponibles=d['cupos_disponibles'],
                politica_id=d.get('politica_id', 1)
            )
            for d in destinos
        ]
    
    def buscar_por_nombre(self, nombre: str) -> list[DestinoDTO]:
        """Busca destinos activos por nombre (LIKE)."""
        sql = "SELECT * FROM Destinos WHERE nombre LIKE %s AND activo = 1"
        params = (f"%{nombre}%",)
        destinos = ejecutar_consulta(sql, params)
        
        if not destinos:
            return []
        
        return [
            DestinoDTO(
                id=d['id'],
                nombre=d['nombre'],
                descripcion=d['descripcion'],
                costo_base=d['costo_base'],
                cupos_disponibles=d['cupos_disponibles'],
                politica_id=d.get('politica_id', 1)
            )
            for d in destinos
        ]
    
    def reducir_cupo(self, id: int) -> bool:
        """Reduce en 1 el cupo disponible del destino."""
        sql = "UPDATE Destinos SET cupos_disponibles = cupos_disponibles - 1 WHERE id=%s AND cupos_disponibles > 0"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def aumentar_cupo(self, id: int) -> bool:
        """Aumenta en 1 el cupo disponible del destino."""
        sql = "UPDATE Destinos SET cupos_disponibles = cupos_disponibles + 1 WHERE id=%s"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0