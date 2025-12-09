"""Service Layer para Paquetes

Encapsula la lógica de negocio relacionada con paquetes turísticos.
Intermediario entre la UI y el DAO para mantener separación de capas.
"""

from datetime import datetime

from src.dao.paquete_actividad_dao import PaqueteActividadDAO
from src.dao.paquete_dao import PaqueteDAO
from src.dto.paquete_dto import PaqueteDTO
from src.utils.exceptions import ValidacionError


class PaqueteService:
    """Servicio para gestión de paquetes turísticos."""
    
    def __init__(self, paquete_dao: PaqueteDAO | None = None):
        """Inicializa el servicio con su DAO. Permite inyección de dependencias."""
        self.paquete_dao = paquete_dao or PaqueteDAO()
        self.paquete_actividad_dao = PaqueteActividadDAO()
    
    def crear_paquete(
        self,
        nombre: str,
        descripcion: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        precio_total: int,
        cupos_disponibles: int,
        politica_id: int,
        destino_id: int | None = None
    ) -> PaqueteDTO:
        """Crea un nuevo paquete con validaciones. Retorna PaqueteDTO con el paquete creado"""
        # Validaciones de negocio
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del paquete no puede estar vacío")
        if precio_total <= 0:
            raise ValidacionError("El precio total debe ser mayor a 0")
        if cupos_disponibles < 0:
            raise ValidacionError("Los cupos disponibles no pueden ser negativos")
        if fecha_fin <= fecha_inicio:
            raise ValidacionError("La fecha de fin debe ser posterior a la fecha de inicio")
        
        # Validar que la fecha de inicio no esté en el pasado
        hoy = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if fecha_inicio < hoy:
            raise ValidacionError("La fecha de inicio no puede estar en el pasado")
        
        if politica_id <= 0:
            raise ValidacionError("Debe especificar una política de cancelación válida")
        
        # Crear DTO y delegar al DAO
        paquete = PaqueteDTO(
            id=None,
            nombre=nombre.strip(),
            descripcion=(descripcion or "").strip(),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            precio_total=precio_total,
            cupos_disponibles=cupos_disponibles,
            politica_id=politica_id
        )
        
        paquete_id = self.paquete_dao.crear(paquete)
        paquete.id = paquete_id
        
        # Asociar destino al paquete si se proporcionó
        if destino_id:
            self.paquete_dao.agregar_destino(paquete_id, destino_id)
        
        return paquete
    
    def obtener_paquete(self, paquete_id: int) -> PaqueteDTO | None:
        """Obtiene un paquete por ID. Retorna PaqueteDTO o None si no existe"""
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        return self.paquete_dao.obtener_por_id(paquete_id)
    
    def listar_todos_paquetes(self) -> list[PaqueteDTO]:
        """Lista todos los paquetes activos. Retorna Lista de PaqueteDTO"""
        return self.paquete_dao.listar_todos()
    
    def listar_todos_paquetes_admin(self) -> list[dict]:
        """Lista TODOS los paquetes incluyendo inactivos (para admin). Retorna Lista de dicts con info de paquetes"""
        return self.paquete_dao.listar_todos_admin()
    
    def listar_paquetes_disponibles(self) -> list[PaqueteDTO]:
        """Lista paquetes activos con cupos disponibles. Retorna Lista de PaqueteDTO con cupos > 0"""
        todos = self.paquete_dao.listar_todos()
        return [p for p in todos if p.cupos_disponibles > 0]
    
    def reactivar_paquete(self, paquete_id: int) -> bool:
        """Reactiva un paquete desactivado. Retorna True si se reactivó correctamente"""
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        return self.paquete_dao.reactivar(paquete_id)
    
    def actualizar_paquete(
        self,
        paquete_id: int,
        nombre: str,
        descripcion: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        precio_total: int,
        cupos_disponibles: int,
        politica_id: int
    ) -> PaqueteDTO:
        """Actualiza un paquete existente. Retorna PaqueteDTO actualizado"""
        # Validaciones
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del paquete no puede estar vacío")
        if not descripcion or not descripcion.strip():
            raise ValidacionError("La descripción no puede estar vacía")
        if precio_total <= 0:
            raise ValidacionError("El precio total debe ser mayor a 0")
        if cupos_disponibles < 0:
            raise ValidacionError("Los cupos disponibles no pueden ser negativos")
        if fecha_fin <= fecha_inicio:
            raise ValidacionError("La fecha de fin debe ser posterior a la fecha de inicio")
        if politica_id <= 0:
            raise ValidacionError("Debe especificar una política de cancelación válida")
        
        # Verificar existencia
        paquete_existente = self.paquete_dao.obtener_por_id(paquete_id)
        if not paquete_existente:
            raise ValidacionError(f"No existe un paquete con ID {paquete_id}")
        
        # Actualizar
        paquete = PaqueteDTO(
            id=paquete_id,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            precio_total=precio_total,
            cupos_disponibles=cupos_disponibles,
            politica_id=politica_id
        )
        
        success = self.paquete_dao.actualizar(paquete_id, paquete)
        if not success:
            raise ValidacionError(f"No se pudo actualizar el paquete con ID {paquete_id}")
        return paquete
    
    def eliminar_paquete(self, paquete_id: int) -> bool:
        """Elimina un paquete. Retorna True si se eliminó correctamente"""
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        # Verificar existencia
        paquete_existente = self.paquete_dao.obtener_por_id(paquete_id)
        if not paquete_existente:
            raise ValidacionError(f"No existe un paquete con ID {paquete_id}")
        
        return self.paquete_dao.eliminar(paquete_id)
    
    def obtener_actividades_paquete(self, paquete_id: int) -> list:
        """Obtiene las actividades de un paquete. Retorna Lista de actividades asociadas al paquete"""
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        return self.paquete_dao.obtener_actividades_paquete(paquete_id)

    def obtener_destinos_paquete(self, paquete_id: int) -> list[dict]:
        """Obtiene los destinos de un paquete. Retorna Lista de destinos asociados"""
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        return self.paquete_dao.listar_destinos_paquete(paquete_id)
