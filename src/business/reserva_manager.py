"""Gestor de Reservas - Business Logic"""

from src.dao.paquete_dao import PaqueteDAO
from src.dao.reserva_dao import ReservaDAO
from src.dto.paquete_dto import PaqueteDTO
from src.dto.reserva_dto import ReservaDTO
from src.utils.constants import ESTADOS_RESERVA


def crear_reserva(usuario_id: int, paquete_id: int, num_personas: int, fecha_viaje: str) -> int:
    """Crea una reserva y reduce cupos del paquete."""
    ...


def confirmar_reserva(reserva_id: int) -> bool:
    """Confirma una reserva pendiente cambiando su estado."""
    ...


def cancelar_reserva(reserva_id: int) -> bool:
    """Cancela una reserva y devuelve los cupos al paquete."""
    ...


def obtener_reservas_cliente(usuario_id: int) -> list[ReservaDTO]:
    """Retorna todas las reservas de un cliente."""
    ...


def calcular_precio_total(paquete_id: int, num_personas: int) -> float:
    """Calcula el precio total de una reserva (precio_paquete * num_personas)."""
    ...


def verificar_disponibilidad(paquete_id: int, num_personas: int) -> bool:
    """Verifica si hay cupos disponibles en el paquete para el número de personas."""
    ...


def obtener_detalle_reserva(reserva_id: int) -> ReservaDTO | None:
    """Obtiene los detalles completos de una reserva."""
    ...        