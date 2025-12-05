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
        """Obtiene una política por ID.
        
        Args:
            id: ID de la política a buscar
            
        Returns:
            PoliticaCancelacionDTO si se encuentra, None si no existe
        """
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
        """Retorna todas las políticas de cancelación.
        
        Returns:
            Lista de PoliticaCancelacionDTO ordenadas por ID
        """
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
