"""Service Layer para Destinos

Encapsula la lógica de negocio relacionada con destinos.
Intermediario entre la UI y el DAO para mantener separación de capas.
"""

from src.dao.destino_dao import DestinoDAO
from src.dto.destino_dto import DestinoDTO
from src.utils.exceptions import ValidacionError


class DestinoService:
    '''Servicio para gestión de destinos.'''
    
    def __init__(self, destino_dao: DestinoDAO | None = None):
        '''Inicializa el servicio con su DAO. Permite inyección de dependencias.'''
        self.destino_dao = destino_dao or DestinoDAO()
    
    def crear_destino(
        self,
        nombre: str,
        pais: str,
        descripcion: str,
        costo_base: int,
        cupos_disponibles: int = 50,
        politica_id: int = 1
    ) -> DestinoDTO:
        '''Crea un nuevo destino con validaciones. Retorna DestinoDTO con el destino creado'''
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
        '''Obtiene un destino por su ID. Retorna DestinoDTO o None si no existe'''
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        
        return self.destino_dao.obtener_por_id(destino_id)
    
    def listar_todos_destinos(self) -> list[DestinoDTO]:
        '''Lista todos los destinos activos. Retorna lista de DestinoDTO'''
        return self.destino_dao.listar_todos()
    
    def listar_destinos_disponibles(self) -> list[DestinoDTO]:
        '''Lista destinos con cupos disponibles. Retorna lista de DestinoDTO'''
        todos = self.destino_dao.listar_todos()
        return [d for d in todos if d.cupos_disponibles > 0]
    
    def actualizar_destino(
        self,
        destino_id: int,
        nombre: str,
        pais: str,
        descripcion: str,
        costo_base: int,
        cupos_disponibles: int,
        politica_id: int | None
    ) -> DestinoDTO:
        '''Actualiza un destino existente con validaciones. Retorna el DestinoDTO actualizado'''
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
        '''Elimina un destino por su ID. Retorna True si se eliminó correctamente'''
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        
        # Verificar existencia
        destino_existente = self.destino_dao.obtener_por_id(destino_id)
        if not destino_existente:
            raise ValidacionError(f"No existe un destino con ID {destino_id}")
        
        return self.destino_dao.eliminar(destino_id)
    
    def buscar_destinos_por_nombre(self, nombre: str) -> list[DestinoDTO]:
        '''Busca destinos por nombre (parcial, case-insensitive). Retorna lista de DestinoDTO'''
        if not nombre or not nombre.strip():
            raise ValidacionError("El nombre no puede estar vacío")
        
        return self.destino_dao.buscar_por_nombre(nombre.strip())
