"""Service Layer para Actividades

Encapsula la lógica de negocio relacionada con actividades turísticas.
Intermediario entre la UI y el DAO para mantener separación de capas.
"""

from src.dao.actividad_dao import ActividadDAO
from src.dto.actividad_dto import ActividadDTO
from src.utils.exceptions import ValidacionError


class ActividadService:
    """Servicio para gestión de actividades turísticas."""
    
    def __init__(self):
        """Inicializa el servicio con su DAO."""
        self.actividad_dao = ActividadDAO()
    
    def crear_actividad(
        self,
        nombre: str,
        descripcion: str,
        duracion_horas: int,
        precio_base: int,
        destino_id: int
    ) -> ActividadDTO:
        """Crea una nueva actividad con validaciones.
        
        Args:
            nombre: Nombre de la actividad
            descripcion: Descripción de la actividad
            duracion_horas: Duración en horas
            precio_base: Precio base de la actividad
            destino_id: ID del destino asociado
            
        Returns:
            ActividadDTO con la actividad creada
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones de negocio
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre de la actividad no puede estar vacío")
        if not descripcion or not descripcion.strip():
            raise ValidacionError("La descripción no puede estar vacía")
        if duracion_horas <= 0:
            raise ValidacionError("La duración debe ser mayor a 0 horas")
        if precio_base < 0:
            raise ValidacionError("El precio base no puede ser negativo")
        if destino_id <= 0:
            raise ValidacionError("Debe especificar un destino válido")
        
        # Crear DTO y delegar al DAO
        actividad = ActividadDTO(
            id=None,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            duracion_horas=duracion_horas,
            precio_base=precio_base,
            destino_id=destino_id
        )
        
        actividad_id = self.actividad_dao.crear(actividad)
        actividad.id = actividad_id
        return actividad
    
    def obtener_actividad(self, actividad_id: int) -> ActividadDTO | None:
        """Obtiene una actividad por ID.
        
        Args:
            actividad_id: ID de la actividad
            
        Returns:
            ActividadDTO o None si no existe
        """
        if actividad_id <= 0:
            raise ValidacionError("El ID de la actividad debe ser mayor a 0")
        
        return self.actividad_dao.obtener_por_id(actividad_id)
    
    def listar_todas_actividades(self) -> list[ActividadDTO]:
        """Lista todas las actividades.
        
        Returns:
            Lista de ActividadDTO
        """
        return self.actividad_dao.listar_todas()
    
    def listar_actividades_por_destino(self, destino_id: int) -> list[ActividadDTO]:
        """Lista actividades de un destino específico.
        
        Args:
            destino_id: ID del destino
            
        Returns:
            Lista de ActividadDTO del destino
        """
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        
        return self.actividad_dao.listar_por_destino(destino_id)
    
    def actualizar_actividad(
        self,
        actividad_id: int,
        nombre: str,
        descripcion: str,
        duracion_horas: int,
        precio_base: int,
        destino_id: int
    ) -> ActividadDTO:
        """Actualiza una actividad existente.
        
        Args:
            actividad_id: ID de la actividad a actualizar
            nombre: Nuevo nombre
            descripcion: Nueva descripción
            duracion_horas: Nueva duración
            precio_base: Nuevo precio base
            destino_id: Nuevo ID de destino
            
        Returns:
            ActividadDTO actualizada
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones
        if actividad_id <= 0:
            raise ValidacionError("El ID de la actividad debe ser mayor a 0")
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre de la actividad no puede estar vacío")
        if not descripcion or not descripcion.strip():
            raise ValidacionError("La descripción no puede estar vacía")
        if duracion_horas <= 0:
            raise ValidacionError("La duración debe ser mayor a 0 horas")
        if precio_base < 0:
            raise ValidacionError("El precio base no puede ser negativo")
        if destino_id <= 0:
            raise ValidacionError("Debe especificar un destino válido")
        
        # Verificar existencia
        actividad_existente = self.actividad_dao.obtener_por_id(actividad_id)
        if not actividad_existente:
            raise ValidacionError(f"No existe una actividad con ID {actividad_id}")
        
        # Actualizar
        actividad = ActividadDTO(
            id=actividad_id,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            duracion_horas=duracion_horas,
            precio_base=precio_base,
            destino_id=destino_id
        )
        
        success = self.actividad_dao.actualizar(actividad_id, actividad)
        if not success:
            raise ValidacionError(f"No se pudo actualizar la actividad con ID {actividad_id}")
        return actividad
    
    def eliminar_actividad(self, actividad_id: int) -> bool:
        """Elimina una actividad.
        
        Args:
            actividad_id: ID de la actividad a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValidacionError: Si el ID no es válido
        """
        if actividad_id <= 0:
            raise ValidacionError("El ID de la actividad debe ser mayor a 0")
        
        # Verificar existencia
        actividad_existente = self.actividad_dao.obtener_por_id(actividad_id)
        if not actividad_existente:
            raise ValidacionError(f"No existe una actividad con ID {actividad_id}")
        
        return self.actividad_dao.eliminar(actividad_id)
