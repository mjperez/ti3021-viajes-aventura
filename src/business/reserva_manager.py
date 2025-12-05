"""Gestor de Reservas - Business Logic"""

from datetime import datetime

from src.dao.destino_dao import DestinoDAO
from src.dao.paquete_dao import PaqueteDAO
from src.dao.reserva_dao import ReservaDAO
from src.dto.reserva_dto import ReservaDTO
from src.utils.constants import ESTADOS_RESERVA


def crear_reserva(usuario_id: int, paquete_id: int, num_personas: int) -> int:
    """Crea una reserva y reduce cupos del paquete."""
    paquete_dao = PaqueteDAO()
    reserva_dao = ReservaDAO()
    
    # Validar que el paquete existe
    paquete = paquete_dao.obtener_por_id(paquete_id)
    if not paquete:
        raise ValueError("El paquete no existe")
    
    # Verificar disponibilidad
    if not verificar_disponibilidad(paquete_id, num_personas):
        raise ValueError("No hay cupos suficientes disponibles")
    
    # Calcular precio total
    precio_total = calcular_precio_total(paquete_id, num_personas)
    
    # Crear DTO de reserva
    reserva = ReservaDTO(
        id=0,  # Se asigna en BD
        fecha_reserva=datetime.now(),  # Fecha actual
        estado=ESTADOS_RESERVA[0],  # "Pendiente"
        monto_total=precio_total,
        numero_personas=num_personas,
        usuario_id=usuario_id,
        paquete_id=paquete_id
    )
    
    try:
        # Crear reserva
        reserva_id = reserva_dao.crear(reserva)
        
        # Reducir cupos del paquete (uno a uno)
        for _ in range(num_personas):
            if not paquete_dao.reducir_cupo(paquete_id):
                # Si falla, devolver los cupos ya reducidos
                for _ in range(_):
                    paquete_dao.aumentar_cupo(paquete_id)
                raise ValueError("Error al reducir cupos del paquete")
        
        return reserva_id
    except Exception as e:
        raise ValueError(f"Error al crear reserva: {str(e)}")


def confirmar_reserva(reserva_id: int) -> bool:
    """Confirma una reserva pendiente cambiando su estado."""
    reserva_dao = ReservaDAO()
    
    # Verificar que la reserva existe
    reserva = reserva_dao.obtener_por_id(reserva_id)
    if not reserva:
        raise ValueError("La reserva no existe")
    
    # Verificar que está en estado Pendiente
    if reserva.estado != ESTADOS_RESERVA[0]:  # "Pendiente"
        raise ValueError(f"La reserva debe estar en estado Pendiente. Estado actual: {reserva.estado}")
    
    # Confirmar la reserva
    return reserva_dao.confirmar(reserva_id)


def cancelar_reserva(reserva_id: int) -> bool:
    """Cancela una reserva y devuelve los cupos al paquete o destino."""
    reserva_dao = ReservaDAO()
    paquete_dao = PaqueteDAO()
    destino_dao = DestinoDAO()
    
    # Obtener la reserva
    reserva = reserva_dao.obtener_por_id(reserva_id)
    if not reserva:
        raise ValueError("La reserva no existe")
    
    # Verificar que no esté ya cancelada
    if reserva.estado == ESTADOS_RESERVA[3]:  # "Cancelada"
        raise ValueError("La reserva ya está cancelada")
    
    # Cancelar la reserva
    if not reserva_dao.cancelar(reserva_id):
        return False
    
    # Devolver los cupos según el tipo de reserva
    if reserva.paquete_id:
        # Reserva de paquete: devolver cupos al paquete
        for _ in range(reserva.numero_personas):
            paquete_dao.aumentar_cupo(reserva.paquete_id)
    elif reserva.destino_id:
        # Reserva de destino: devolver cupos al destino
        for _ in range(reserva.numero_personas):
            destino_dao.aumentar_cupo(reserva.destino_id)
    
    return True


def obtener_reservas_cliente(usuario_id: int) -> list[ReservaDTO]:
    """Retorna todas las reservas de un cliente."""
    reserva_dao = ReservaDAO()
    return reserva_dao.listar_por_cliente(usuario_id)


def calcular_precio_total(paquete_id: int, num_personas: int) -> float:
    """Calcula el precio total de una reserva (precio_paquete * num_personas)."""
    paquete_dao = PaqueteDAO()
    
    paquete = paquete_dao.obtener_por_id(paquete_id)
    if not paquete:
        raise ValueError("El paquete no existe")
    
    return paquete.precio_total * num_personas


def verificar_disponibilidad(paquete_id: int, num_personas: int) -> bool:
    """Verifica si hay cupos disponibles en el paquete para el número de personas."""
    paquete_dao = PaqueteDAO()
    
    paquete = paquete_dao.obtener_por_id(paquete_id)
    if not paquete:
        return False
    
    return paquete.cupos_disponibles >= num_personas


def obtener_detalle_reserva(reserva_id: int) -> ReservaDTO | None:
    """Obtiene los detalles completos de una reserva."""
    reserva_dao = ReservaDAO()
    return reserva_dao.obtener_por_id(reserva_id)


# ========== FUNCIONES PARA RESERVAS DE DESTINOS ========== #

def crear_reserva_destino(usuario_id: int, destino_id: int, num_personas: int) -> int:
    """Crea una reserva de destino individual y reduce cupos."""
    destino_dao = DestinoDAO()
    reserva_dao = ReservaDAO()
    
    # Validar que el destino existe
    destino = destino_dao.obtener_por_id(destino_id)
    if not destino:
        raise ValueError("El destino no existe")
    
    # Verificar disponibilidad
    if not verificar_disponibilidad_destino(destino_id, num_personas):
        raise ValueError("No hay cupos suficientes disponibles en este destino")
    
    # Calcular precio total
    precio_total = calcular_precio_destino(destino_id, num_personas)
    
    # Crear DTO de reserva
    reserva = ReservaDTO(
        id=0,  # Se asigna en BD
        fecha_reserva=datetime.now(),
        estado=ESTADOS_RESERVA[0],  # "PENDIENTE"
        monto_total=precio_total,
        numero_personas=num_personas,
        usuario_id=usuario_id,
        destino_id=destino_id
    )
    
    try:
        # Crear reserva
        reserva_id = reserva_dao.crear(reserva)
        
        # Reducir cupos del destino (uno a uno)
        for _ in range(num_personas):
            if not destino_dao.reducir_cupo(destino_id):
                # Si falla, devolver los cupos ya reducidos
                for _ in range(_):
                    destino_dao.aumentar_cupo(destino_id)
                raise ValueError("Error al reducir cupos del destino")
        
        return reserva_id
    except Exception as e:
        raise ValueError(f"Error al crear la reserva de destino: {str(e)}")


def calcular_precio_destino(destino_id: int, num_personas: int) -> float:
    """Calcula el precio total de una reserva de destino."""
    destino_dao = DestinoDAO()
    
    destino = destino_dao.obtener_por_id(destino_id)
    if not destino:
        raise ValueError("El destino no existe")
    
    return destino.costo_base * num_personas


def verificar_disponibilidad_destino(destino_id: int, num_personas: int) -> bool:
    """Verifica si hay cupos disponibles en el destino."""
    destino_dao = DestinoDAO()
    
    destino = destino_dao.obtener_por_id(destino_id)
    if not destino:
        return False
    
    return destino.cupos_disponibles >= num_personas