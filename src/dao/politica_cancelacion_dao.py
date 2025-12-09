"""DAO para Políticas de Cancelación - Data Access Object

Maneja operaciones de base de datos para políticas de cancelación.
"""

from src.config.db_connection import (
    ejecutar_consulta,
    ejecutar_consulta_uno,
)
from src.dto.politica_cancelacion_dto import PoliticaCancelacionDTO


class PoliticaCancelacionDAO:
    """Maneja operaciones de base de datos para Políticas de Cancelación."""
    
    def obtener_por_id(self, id: int) -> PoliticaCancelacionDTO | None:
        """Obtiene una política por ID. Retorna PoliticaCancelacionDTO si se encuentra, None si no existe"""
        sql = "SELECT * FROM PoliticasCancelacion WHERE id = %s"
        politica = ejecutar_consulta_uno(sql, (id,))
        
        if not politica:
            return None
        
        return PoliticaCancelacionDTO(
            id=politica['id'],
            nombre=politica['nombre'],
            dias_aviso=politica['dias_aviso'],
            porcentaje_reembolso=politica['porcentaje_reembolso']
        )
    
    def listar_todas(self) -> list[PoliticaCancelacionDTO]:
        """Retorna todas las políticas de cancelación. Retorna Lista de PoliticaCancelacionDTO ordenadas por ID"""
        sql = "SELECT * FROM PoliticasCancelacion ORDER BY id ASC"
        politicas = ejecutar_consulta(sql)
        
        if not politicas:
            return []
        
        return [
            PoliticaCancelacionDTO(
                id=p['id'],
                nombre=p['nombre'],
                dias_aviso=p['dias_aviso'],
                porcentaje_reembolso=p['porcentaje_reembolso']
            )
            for p in politicas
        ]
    
    def crear(self, nombre: str, dias_aviso: int, porcentaje_reembolso: float) -> PoliticaCancelacionDTO:
        """Crea una nueva política de cancelación. Retorna PoliticaCancelacionDTO con la política creada"""
        from src.config.db_connection import ejecutar_insercion
        
        sql = """INSERT INTO PoliticasCancelacion (nombre, dias_aviso, porcentaje_reembolso) 
                 VALUES (%s, %s, %s)"""
        politica_id = ejecutar_insercion(sql, (nombre, dias_aviso, porcentaje_reembolso))
        
        return PoliticaCancelacionDTO(
            id=politica_id,
            nombre=nombre,
            dias_aviso=dias_aviso,
            porcentaje_reembolso=porcentaje_reembolso
        )
    
    def actualizar(self, id: int, nombre: str, dias_aviso: int, porcentaje_reembolso: float) -> PoliticaCancelacionDTO:
        """Actualiza una política de cancelación existente. Retorna PoliticaCancelacionDTO con los datos actualizados"""
        from src.config.db_connection import ejecutar_actualizacion
        
        sql = """UPDATE PoliticasCancelacion 
                 SET nombre = %s, dias_aviso = %s, porcentaje_reembolso = %s 
                 WHERE id = %s"""
        ejecutar_actualizacion(sql, (nombre, dias_aviso, porcentaje_reembolso, id))
        
        return PoliticaCancelacionDTO(
            id=id,
            nombre=nombre,
            dias_aviso=dias_aviso,
            porcentaje_reembolso=porcentaje_reembolso
        )
    
    def eliminar(self, id: int) -> bool:
        """Elimina una política de cancelación. Retorna True si se eliminó correctamente"""
        from src.config.db_connection import ejecutar_actualizacion
        
        sql = "DELETE FROM PoliticasCancelacion WHERE id = %s"
        filas_afectadas = ejecutar_actualizacion(sql, (id,))
        return filas_afectadas > 0
