from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.actividad_dto import ActividadDTO


class ActividadDAO():
    #Maneja todas las operaciones de base de datos relacionadas con Actividades.
    
    def crear(self, actividad_dto: ActividadDTO) -> int: 
        #Inserta una nueva actividad
        sql = "INSERT INTO Actividades (nombre, descripcion, duracion_horas, precio_base, destino_id) VALUES (%s,%s,%s,%s,%s)"
        params = (actividad_dto.nombre, actividad_dto.descripcion, actividad_dto.duracion_horas, actividad_dto.precio_base, actividad_dto.destino_id)
        return ejecutar_insercion(sql, params)
    
    def obtener_por_id(self, id: int) -> ActividadDTO | None: 
        #Busca actividad por ID
        sql = "SELECT * FROM Actividades WHERE id=%s"
        params = (id,)
        actividad = ejecutar_consulta_uno(sql, params)
        
        if not actividad:
            return None
        
        return ActividadDTO(
            id=actividad['id'],
            nombre=actividad['nombre'],
            descripcion=actividad['descripcion'],
            duracion_horas=actividad['duracion_horas'],
            precio_base=actividad['precio_base'],
            destino_id=actividad['destino_id']
        )
    
    def actualizar(self, id: int, actividad_dto: ActividadDTO) -> bool: 
        #Actualiza datos de la actividad
        sql = "UPDATE Actividades SET nombre=%s, descripcion=%s, duracion_horas=%s, precio_base=%s, destino_id=%s WHERE id=%s"
        params = (actividad_dto.nombre, actividad_dto.descripcion, actividad_dto.duracion_horas, actividad_dto.precio_base, actividad_dto.destino_id, id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def eliminar(self, id: int) -> bool: 
        #Elimina una actividad
        sql = "DELETE FROM Actividades WHERE id=%s"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def listar_todas(self) -> list[ActividadDTO]:
        #Retorna lista de todas las actividades
        sql = "SELECT * FROM Actividades ORDER BY id ASC"
        actividades = ejecutar_consulta(sql)        
        if not actividades:
            return []
        
        return [
            ActividadDTO(
                id=a['id'],
                nombre=a['nombre'],
                descripcion=a['descripcion'],
                duracion_horas=a['duracion_horas'],
                precio_base=a['precio_base'],
                destino_id=a['destino_id']
            )
            for a in actividades
        ]
    
    def listar_por_destino(self, destino_id: int) -> list[ActividadDTO]: 
        #Retorna actividades de un destino específico
        sql = "SELECT * FROM Actividades WHERE destino_id=%s"
        params = (destino_id,)
        actividades = ejecutar_consulta(sql, params)
        
        if not actividades:
            return []
        
        return [
            ActividadDTO(
                id=a['id'],
                nombre=a['nombre'],
                descripcion=a['descripcion'],
                duracion_horas=a['duracion_horas'],
                precio_base=a['precio_base'],
                destino_id=a['destino_id']
            )
            for a in actividades
        ]