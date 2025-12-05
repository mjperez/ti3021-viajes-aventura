"""Service Layer para Destinos

Encapsula la lógica de negocio relacionada con destinos.
Intermediario entre la UI y el DAO para mantener separación de capas.
"""

from src.dao.destino_dao import DestinoDAO
from src.dto.destino_dto import DestinoDTO
from src.utils.exceptions import ValidacionError


class DestinoService:
    """Servicio para gestión de destinos."""
    
    def __init__(self):
        """Inicializa el servicio con su DAO."""
        self.destino_dao = DestinoDAO()
    
    def crear_destino(
        self,
        nombre: str,
        pais: str,
        descripcion: str,
        costo_base: float,
        cupos_disponibles: int = 50,
        politica_id: int = 1
    ) -> DestinoDTO:
        """Crea un nuevo destino con validaciones.
        
        Args:
            nombre: Nombre del destino
            pais: País del destino
            descripcion: Descripción del destino
            costo_base: Costo base del destino
            cupos_disponibles: Cupos disponibles (default 50)
            politica_id: ID de la política de cancelación (default 1=Flexible)
            
        Returns:
            DestinoDTO con el destino creado
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones de negocio
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del destino no puede estar vacío")
        if not pais or not pais.strip():
            raise ValidacionError("El país no puede estar vacío")
        if not descripcion or not descripcion.strip():
            raise ValidacionError("La descripción no puede estar vacía")
        if costo_base <= 0:
            raise ValidacionError("El costo base debe ser mayor a 0")
        if cupos_disponibles < 0:
            raise ValidacionError("Los cupos disponibles no pueden ser negativos")
        if politica_id <= 0:
            raise ValidacionError("El ID de política debe ser mayor a 0")
        
        # Crear DTO y delegar al DAO
        destino = DestinoDTO(
            id=None,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            costo_base=costo_base,
            cupos_disponibles=cupos_disponibles,
            politica_id=politica_id
        )
        
        destino_id = self.destino_dao.crear(destino)
        destino.id = destino_id
        return destino
    
    def obtener_destino(self, destino_id: int) -> DestinoDTO | None:
        """Obtiene un destino por ID.
        
        Args:
            destino_id: ID del destino
            
        Returns:
            DestinoDTO o None si no existe
        """
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        
        return self.destino_dao.obtener_por_id(destino_id)
    
    def listar_todos_destinos(self) -> list[DestinoDTO]:
        """Lista todos los destinos.
        
        Returns:
            Lista de DestinoDTO
        """
        return self.destino_dao.listar_todos()
    
    def listar_destinos_disponibles(self) -> list[DestinoDTO]:
        """Lista destinos con cupos disponibles.
        
        Returns:
            Lista de DestinoDTO con cupos > 0
        """
        todos = self.destino_dao.listar_todos()
        return [d for d in todos if d.cupos_disponibles > 0]
    
    def actualizar_destino(
        self,
        destino_id: int,
        nombre: str,
        pais: str,
        descripcion: str,
        costo_base: float,
        cupos_disponibles: int,
        politica_id: int = None
    ) -> DestinoDTO:
        """Actualiza un destino existente.
        
        Args:
            destino_id: ID del destino a actualizar
            nombre: Nuevo nombre
            pais: Nuevo país
            descripcion: Nueva descripción
            costo_base: Nuevo costo base
            cupos_disponibles: Nuevos cupos disponibles
            politica_id: Nueva política de cancelación (None para mantener)
            
        Returns:
            DestinoDTO actualizado
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre del destino no puede estar vacío")
        if not pais or not pais.strip():
            raise ValidacionError("El país no puede estar vacío")
        if not descripcion or not descripcion.strip():
            raise ValidacionError("La descripción no puede estar vacía")
        if costo_base <= 0:
            raise ValidacionError("El costo base debe ser mayor a 0")
        if cupos_disponibles < 0:
            raise ValidacionError("Los cupos disponibles no pueden ser negativos")
        
        # Verificar existencia
        destino_existente = self.destino_dao.obtener_por_id(destino_id)
        if not destino_existente:
            raise ValidacionError(f"No existe un destino con ID {destino_id}")
        
        # Usar política existente si no se especifica
        if politica_id is None:
            politica_id = destino_existente.politica_id
        
        # Actualizar
        destino = DestinoDTO(
            id=destino_id,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            costo_base=costo_base,
            cupos_disponibles=cupos_disponibles,
            politica_id=politica_id
        )
        
        success = self.destino_dao.actualizar(destino_id, destino)
        if not success:
            raise ValidacionError(f"No se pudo actualizar el destino con ID {destino_id}")
        return destino
    
    def eliminar_destino(self, destino_id: int) -> bool:
        """Elimina un destino.
        
        Args:
            destino_id: ID del destino a eliminar
            
        Returns:
            True si se eliminó correctamente
            
        Raises:
            ValidacionError: Si el ID no es válido
        """
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        
        # Verificar existencia
        destino_existente = self.destino_dao.obtener_por_id(destino_id)
        if not destino_existente:
            raise ValidacionError(f"No existe un destino con ID {destino_id}")
        
        return self.destino_dao.eliminar(destino_id)
    
    def buscar_destinos_por_nombre(self, nombre: str) -> list[DestinoDTO]:
        """Busca destinos por nombre.
        
        Args:
            nombre: Nombre a buscar
            
        Returns:
            Lista de DestinoDTO que coinciden con el nombre
        """
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre no puede estar vacío")
        
        return self.destino_dao.buscar_por_nombre(nombre.strip())
