"""Service Layer para Reservas

Encapsula la lógica de negocio relacionada con reservas.
Intermediario entre la UI y el DAO para mantener separación de capas.
Reemplaza completamente a reserva_manager.py (eliminando redundancia).
"""

from datetime import datetime

from src.dao.destino_dao import DestinoDAO
from src.dao.paquete_dao import PaqueteDAO
from src.dao.reserva_dao import ReservaDAO
from src.dto.reserva_dto import ReservaDTO
from src.utils.constants import ESTADOS_RESERVA
from src.utils.exceptions import ValidacionError


class ReservaService:
    """Servicio para gestión de reservas."""
    
    def __init__(self):
        """Inicializa el servicio con sus DAOs."""
        self.reserva_dao = ReservaDAO()
        self.paquete_dao = PaqueteDAO()
        self.destino_dao = DestinoDAO()
    
    def obtener_reserva(self, reserva_id: int) -> ReservaDTO | None:
        """Obtiene una reserva por ID.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            ReservaDTO o None si no existe
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        return self.reserva_dao.obtener_por_id(reserva_id)
    
    def listar_reservas_cliente(self, cliente_id: int) -> list[ReservaDTO]:
        """Lista todas las reservas de un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Lista de ReservaDTO del cliente
        """
        if cliente_id <= 0:
            raise ValidacionError("El ID del cliente debe ser mayor a 0")
        
        return self.reserva_dao.listar_por_cliente(cliente_id)
    
    def listar_reservas_paquete(self, paquete_id: int) -> list[ReservaDTO]:
        """Lista todas las reservas de un paquete.
        
        Args:
            paquete_id: ID del paquete
            
        Returns:
            Lista de ReservaDTO del paquete
        """
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        return self.reserva_dao.listar_por_paquete(paquete_id)
    
    def listar_reservas_destino(self, destino_id: int) -> list[ReservaDTO]:
        """Lista todas las reservas de un destino.
        
        Args:
            destino_id: ID del destino
            
        Returns:
            Lista de ReservaDTO del destino
        """
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        
        return self.reserva_dao.listar_por_destino(destino_id)
    
    def listar_todas_reservas(self) -> list[ReservaDTO]:
        """Lista todas las reservas del sistema.
        
        Returns:
            Lista de todas las ReservaDTO
        """
        return self.reserva_dao.listar_todas()
    
    def cambiar_estado_reserva(self, reserva_id: int, nuevo_estado: str) -> bool:
        """Cambia el estado de una reserva.
        
        Args:
            reserva_id: ID de la reserva
            nuevo_estado: Nuevo estado (PENDIENTE, CONFIRMADA, CANCELADA, etc.)
            
        Returns:
            True si se actualizó correctamente
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        estados_validos = ["PENDIENTE", "CONFIRMADA", "CANCELADA", "COMPLETADA"]
        if nuevo_estado not in estados_validos:
            raise ValidacionError(f"Estado no válido. Debe ser uno de: {', '.join(estados_validos)}")
        
        # Verificar existencia
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError(f"No existe una reserva con ID {reserva_id}")
        
        # Actualizar estado usando el DAO
        # Como no existe actualizar_estado, usamos los métodos específicos
        if nuevo_estado == "CONFIRMADA":
            return self.reserva_dao.confirmar(reserva_id)
        elif nuevo_estado == "CANCELADA":
            return self.reserva_dao.cancelar(reserva_id)
        else:
            # Para otros estados, necesitamos un método genérico en el DAO
            raise ValidacionError(f"Cambio de estado a '{nuevo_estado}' no implementado")
    
    # ========== NUEVOS MÉTODOS MIGRADOS DE reserva_manager.py ========== #
    
    def crear_reserva_paquete(self, usuario_id: int, paquete_id: int, num_personas: int) -> int:
        """Crea una reserva de paquete y reduce cupos.
        
        Args:
            usuario_id: ID del usuario
            paquete_id: ID del paquete
            num_personas: Número de personas
            
        Returns:
            ID de la reserva creada
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones
        if usuario_id <= 0:
            raise ValidacionError("El ID del usuario debe ser mayor a 0")
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        if num_personas <= 0:
            raise ValidacionError("El número de personas debe ser mayor a 0")
        
        # Validar que el paquete existe
        paquete = self.paquete_dao.obtener_por_id(paquete_id)
        if not paquete:
            raise ValidacionError("El paquete no existe")
        
        # Verificar disponibilidad
        if paquete.cupos_disponibles < num_personas:
            raise ValidacionError("No hay cupos suficientes disponibles")
        
        # Calcular precio total
        precio_total = paquete.precio_total * num_personas
        
        # Crear DTO de reserva
        reserva = ReservaDTO(
            id=None,
            fecha_reserva=datetime.now(),
            estado=ESTADOS_RESERVA[0],  # "PENDIENTE"
            monto_total=precio_total,
            numero_personas=num_personas,
            usuario_id=usuario_id,
            paquete_id=paquete_id,
            destino_id=None
        )
        
        try:
            # Crear reserva
            reserva_id = self.reserva_dao.crear(reserva)
            
            # Reducir cupos del paquete
            for _ in range(num_personas):
                if not self.paquete_dao.reducir_cupo(paquete_id):
                    # Rollback: devolver cupos ya reducidos
                    for _ in range(_):
                        self.paquete_dao.aumentar_cupo(paquete_id)
                    raise ValidacionError("Error al reducir cupos del paquete")
            
            return reserva_id
        except Exception as e:
            raise ValidacionError(f"Error al crear reserva: {str(e)}")
    
    def crear_reserva_destino(self, usuario_id: int, destino_id: int, num_personas: int) -> int:
        """Crea una reserva de destino individual y reduce cupos.
        
        Args:
            usuario_id: ID del usuario
            destino_id: ID del destino
            num_personas: Número de personas
            
        Returns:
            ID de la reserva creada
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones
        if usuario_id <= 0:
            raise ValidacionError("El ID del usuario debe ser mayor a 0")
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        if num_personas <= 0:
            raise ValidacionError("El número de personas debe ser mayor a 0")
        
        # Validar que el destino existe
        destino = self.destino_dao.obtener_por_id(destino_id)
        if not destino:
            raise ValidacionError("El destino no existe")
        
        # Verificar disponibilidad
        if destino.cupos_disponibles < num_personas:
            raise ValidacionError("No hay cupos suficientes disponibles en este destino")
        
        # Calcular precio total
        precio_total = destino.costo_base * num_personas
        
        # Crear DTO de reserva
        reserva = ReservaDTO(
            id=None,
            fecha_reserva=datetime.now(),
            estado=ESTADOS_RESERVA[0],  # "PENDIENTE"
            monto_total=precio_total,
            numero_personas=num_personas,
            usuario_id=usuario_id,
            paquete_id=None,
            destino_id=destino_id
        )
        
        try:
            # Crear reserva
            reserva_id = self.reserva_dao.crear(reserva)
            
            # Reducir cupos del destino
            for _ in range(num_personas):
                if not self.destino_dao.reducir_cupo(destino_id):
                    # Rollback: devolver cupos ya reducidos
                    for _ in range(_):
                        self.destino_dao.aumentar_cupo(destino_id)
                    raise ValidacionError("Error al reducir cupos del destino")
            
            return reserva_id
        except Exception as e:
            raise ValidacionError(f"Error al crear reserva de destino: {str(e)}")
    
    def cancelar_reserva(self, reserva_id: int) -> bool:
        """Cancela una reserva y devuelve los cupos.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            True si se canceló correctamente
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        # Obtener la reserva
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError("La reserva no existe")
        
        # Verificar que no esté ya cancelada
        if reserva.estado == "CANCELADA":
            raise ValidacionError("La reserva ya está cancelada")
        
        # Cancelar la reserva
        if not self.reserva_dao.cancelar(reserva_id):
            return False
        
        # Devolver los cupos según el tipo de reserva
        if reserva.paquete_id:
            # Reserva de paquete: devolver cupos al paquete
            for _ in range(reserva.numero_personas):
                self.paquete_dao.aumentar_cupo(reserva.paquete_id)
        elif reserva.destino_id:
            # Reserva de destino: devolver cupos al destino
            for _ in range(reserva.numero_personas):
                self.destino_dao.aumentar_cupo(reserva.destino_id)
        
        return True
    
    def confirmar_reserva(self, reserva_id: int) -> bool:
        """Confirma una reserva pendiente.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            True si se confirmó correctamente
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        # Verificar que la reserva existe
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError("La reserva no existe")
        
        # Verificar que está en estado Pendiente
        if reserva.estado != "PENDIENTE":
            raise ValidacionError(f"La reserva debe estar en estado PENDIENTE. Estado actual: {reserva.estado}")
        
        # Confirmar la reserva
        return self.reserva_dao.confirmar(reserva_id)
