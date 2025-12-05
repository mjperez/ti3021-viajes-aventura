"""Service Layer para Políticas de Cancelación

Maneja la lógica de negocio para políticas de cancelación.
"""

from src.dao.politica_cancelacion_dao import PoliticaCancelacionDAO
from src.dto.politica_cancelacion_dto import PoliticaCancelacionDTO
from src.utils.exceptions import ValidacionError


class PoliticaCancelacionService:
    """Servicio para gestión de políticas de cancelación."""
    
    def __init__(self):
        """Inicializa el servicio con su DAO."""
        self.politica_dao = PoliticaCancelacionDAO()
    
    def obtener_politica(self, politica_id: int) -> PoliticaCancelacionDTO | None:
        """Obtiene una política por ID.
        
        Args:
            politica_id: ID de la política
            
        Returns:
            PoliticaCancelacionDTO si existe
            
        Raises:
            ValidacionError: Si el ID es inválido
        """
        if politica_id <= 0:
            raise ValidacionError("El ID de la política debe ser mayor a 0")
        
        return self.politica_dao.obtener_por_id(politica_id)
    
    def listar_todas_politicas(self) -> list[PoliticaCancelacionDTO]:
        """Lista todas las políticas disponibles.
        
        Returns:
            Lista de PoliticaCancelacionDTO
        """
        return self.politica_dao.listar_todas()
