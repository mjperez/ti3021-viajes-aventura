"""Service Layer para Paquetes

Encapsula la lógica de negocio relacionada con paquetes turísticos.
Intermediario entre la UI y el DAO para mantener separación de capas.
"""

from datetime import datetime

from src.dao.paquete_dao import PaqueteDAO
from src.dto.paquete_dto import PaqueteDTO
from src.utils.exceptions import ValidacionError


class PaqueteService:
    """Servicio para gestión de paquetes turísticos."""
    
    def __init__(self):
        """Inicializa el servicio con su DAO."""
        self.paquete_dao = PaqueteDAO()
    
    def crear_paquete(
        self,
        nombre: str,
        descripcion: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        precio_total: float,
        cupos_disponibles: int,
        politica_id: int,
        destino_id: int | None = None
    ) -> PaqueteDTO:
        """Crea un nuevo paquete con validaciones.
        
        Args:
            nombre: Nombre del paquete
            descripcion: Descripción del paquete
            fecha_inicio: Fecha de inicio del paquete
            fecha_fin: Fecha de fin del paquete
            precio_total: Precio total del paquete
            cupos_disponibles: Cupos disponibles
            politica_id: ID de la política de cancelación
            destino_id: ID del destino a asociar (opcional)
            
        Returns:
            PaqueteDTO con el paquete creado
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones de negocio
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del paquete no puede estar vacío")
        if precio_total <= 0:
            raise ValidacionError("El precio total debe ser mayor a 0")
        if cupos_disponibles < 0:
            raise ValidacionError("Los cupos disponibles no pueden ser negativos")
        if fecha_fin <= fecha_inicio:
            raise ValidacionError("La fecha de fin debe ser posterior a la fecha de inicio")
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
        """Obtiene un paquete por ID.
        
        Args:
            paquete_id: ID del paquete
            
        Returns:
            PaqueteDTO o None si no existe
        """
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        return self.paquete_dao.obtener_por_id(paquete_id)
    
    def listar_todos_paquetes(self) -> list[PaqueteDTO]:
        """Lista todos los paquetes.
        
        Returns:
            Lista de PaqueteDTO
        """
        return self.paquete_dao.listar_todos()
    
    def listar_paquetes_disponibles(self) -> list[PaqueteDTO]:
        """Lista paquetes con cupos disponibles.
        
        Returns:
            Lista de PaqueteDTO con cupos > 0
        """
        todos = self.paquete_dao.listar_todos()
        return [p for p in todos if p.cupos_disponibles > 0]
    
    def actualizar_paquete(
        self,
        paquete_id: int,
        nombre: str,
        descripcion: str,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        precio_total: float,
        cupos_disponibles: int,
        politica_id: int
    ) -> PaqueteDTO:
        """Actualiza un paquete existente.
        
        Args:
            paquete_id: ID del paquete a actualizar
            nombre: Nuevo nombre
            descripcion: Nueva descripción
            fecha_inicio: Nueva fecha de inicio
            fecha_fin: Nueva fecha de fin
            precio_total: Nuevo precio total
            cupos_disponibles: Nuevos cupos disponibles
            politica_id: Nuevo ID de política
            
        Returns:
            PaqueteDTO actualizado
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
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
        """Elimina un paquete.
        
        Args:
            paquete_id: ID del paquete a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValidacionError: Si el ID no es válido
        """
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        # Verificar existencia
        paquete_existente = self.paquete_dao.obtener_por_id(paquete_id)
        if not paquete_existente:
            raise ValidacionError(f"No existe un paquete con ID {paquete_id}")
        
        return self.paquete_dao.eliminar(paquete_id)
    
    def obtener_actividades_paquete(self, paquete_id: int) -> list:
        """Obtiene las actividades de un paquete.
        
        Args:
            paquete_id: ID del paquete
            
        Returns:
            Lista de actividades con información de destinos
        """
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        return self.paquete_dao.obtener_actividades_paquete(paquete_id)
