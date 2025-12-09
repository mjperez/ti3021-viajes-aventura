"""DAO para la relación Paquete_Actividad.

Maneja la asociación muchos-a-muchos entre Paquetes y Actividades.
"""

from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_insercion,
)


class PaqueteActividadDAO:
    """Maneja operaciones de la tabla Paquete_Actividad."""
    
    def agregar_actividad(self, paquete_id: int, actividad_id: int) -> bool:
        """Asocia una actividad a un paquete. Retorna True si tuvo éxito"""
        sql = "INSERT INTO Paquete_Actividad (paquete_id, actividad_id) VALUES (%s, %s)"
        params = (paquete_id, actividad_id)
        try:
            ejecutar_insercion(sql, params)
            return True
        except Exception:
            return False
    
    def eliminar_actividad(self, paquete_id: int, actividad_id: int) -> bool:
        """Desasocia una actividad de un paquete. Retorna True si se eliminó"""
        sql = "DELETE FROM Paquete_Actividad WHERE paquete_id=%s AND actividad_id=%s"
        params = (paquete_id, actividad_id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def listar_actividades_por_paquete(self, paquete_id: int) -> list[dict]:
        """Retorna actividades asociadas a un paquete con detalles. Retorna Lista de dicts"""
        sql = """
            SELECT a.id, a.nombre, a.descripcion, a.duracion_horas, a.precio_base, a.destino_id
            FROM Actividades a
            JOIN Paquete_Actividad pa ON a.id = pa.actividad_id
            WHERE pa.paquete_id = %s AND a.activo = 1
            ORDER BY a.nombre
        """
        params = (paquete_id,)
        resultados = ejecutar_consulta(sql, params)
        
        if not resultados:
            return []
        
        return [
            {
                'id': r['id'],
                'nombre': r['nombre'],
                'descripcion': r['descripcion'],
                'duracion_horas': r['duracion_horas'],
                'precio_base': r['precio_base'],
                'destino_id': r['destino_id']
            }
            for r in resultados
        ]
    
    def eliminar_todas_actividades(self, paquete_id: int) -> int:
        """Elimina todas las actividades de un paquete. Retorna int con filas afectadas"""
        sql = "DELETE FROM Paquete_Actividad WHERE paquete_id=%s"
        params = (paquete_id,)
        return ejecutar_actualizacion(sql, params)
    
    def existe_asociacion(self, paquete_id: int, actividad_id: int) -> bool:
        """Verifica si una actividad ya está asociada a un paquete. Retorna True si existe asociación"""
        sql = "SELECT COUNT(*) as count FROM Paquete_Actividad WHERE paquete_id=%s AND actividad_id=%s"
        params = (paquete_id, actividad_id)
        from src.config.db_connection import ejecutar_consulta_uno
        resultado = ejecutar_consulta_uno(sql, params)
        return resultado['count'] > 0 if resultado else False
