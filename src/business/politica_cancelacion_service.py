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
        """Obtiene una política por ID. Retorna PoliticaCancelacionDTO si existe"""
        if politica_id <= 0:
            raise ValidacionError("El ID de la política debe ser mayor a 0")
        
        return self.politica_dao.obtener_por_id(politica_id)
    
    def listar_todas_politicas(self) -> list[PoliticaCancelacionDTO]:
        """Lista todas las políticas disponibles. Retorna Lista de PoliticaCancelacionDTO"""
        return self.politica_dao.listar_todas()
    
    def crear_politica(self, nombre: str, dias_aviso: int, porcentaje_reembolso: int) -> PoliticaCancelacionDTO:
        """Crea una nueva política de cancelación. Retorna PoliticaCancelacionDTO con la política creada"""
        from src.utils.validators import (
            validar_dias_aviso,
            validar_porcentaje_reembolso,
        )
        
        if not nombre or len(nombre.strip()) == 0:
            raise ValidacionError("El nombre de la política es requerido")
        
        if not validar_dias_aviso(dias_aviso):
            raise ValidacionError("Los días de aviso deben estar entre 0 y 365")
        
        if not validar_porcentaje_reembolso(porcentaje_reembolso):
            raise ValidacionError("El porcentaje de reembolso debe estar entre 0 y 100")
        
        return self.politica_dao.crear(nombre.strip(), dias_aviso, porcentaje_reembolso)
    
    def actualizar_politica(self, id: int, nombre: str, dias_aviso: int, porcentaje_reembolso: int) -> PoliticaCancelacionDTO:
        """Actualiza una política de cancelación existente. Retorna PoliticaCancelacionDTO con los datos actualizados"""
        from src.utils.validators import (
            validar_dias_aviso,
            validar_porcentaje_reembolso,
        )
        
        if id <= 0:
            raise ValidacionError("El ID de la política debe ser mayor a 0")
        
        # Verificar que la política existe
        politica_existente = self.politica_dao.obtener_por_id(id)
        if not politica_existente:
            raise ValidacionError(f"No existe política con ID {id}")
        
        if not nombre or len(nombre.strip()) == 0:
            raise ValidacionError("El nombre de la política es requerido")
        
        if not validar_dias_aviso(dias_aviso):
            raise ValidacionError("Los días de aviso deben estar entre 0 y 365")
        
        if not validar_porcentaje_reembolso(porcentaje_reembolso):
            raise ValidacionError("El porcentaje de reembolso debe estar entre 0 y 100")
        
        return self.politica_dao.actualizar(id, nombre.strip(), dias_aviso, porcentaje_reembolso)
    
    def eliminar_politica(self, id: int) -> bool:
        """Elimina una política de cancelación. Retorna True si se eliminó correctamente"""
        if id <= 0:
            raise ValidacionError("El ID de la política debe ser mayor a 0")
        
        # Verificar que la política existe
        politica = self.politica_dao.obtener_por_id(id)
        if not politica:
            raise ValidacionError(f"No existe política con ID {id}")
        
        # Verificar si la política está en uso por algún paquete
        from src.config.db_connection import ejecutar_consulta_uno
        sql = "SELECT COUNT(*) as total FROM Paquetes WHERE politica_id = %s"
        resultado = ejecutar_consulta_uno(sql, (id,))
        
        if resultado and resultado['total'] > 0:
            raise ValidacionError(f"No se puede eliminar la política '{politica.nombre}' porque está siendo usada por {resultado['total']} paquete(s)")
        
        return self.politica_dao.eliminar(id)
