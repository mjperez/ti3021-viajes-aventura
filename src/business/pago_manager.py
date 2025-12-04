"""Gestor de Pagos - Business Logic"""

from src.dao.pago_dao import PagoDAO
from src.dao.reserva_dao import ReservaDAO
from src.dto.pago_dto import PagoDTO
from src.utils.constants import ESTADOS_PAGO, METODOS_PAGO


def procesar_pago(reserva_id: int, metodo_pago: str) -> int:
    """Procesa un pago completado y marca la reserva como pagada."""
    ...


def verificar_estado_pago(reserva_id: int) -> bool:
    """Verifica si existe un pago completado para la reserva."""
    ...


def obtener_historial_pagos(reserva_id: int) -> list[PagoDTO]:
    """Retorna el historial de todos los pagos de una reserva."""
    ...


def generar_reporte_ventas(fecha_inicio: str, fecha_fin: str) -> dict:
    """Genera un reporte de ventas con total y listado de pagos en un periodo."""
    ...


def validar_metodo_pago(metodo: str) -> bool:
    """Valida que el método de pago sea uno de los permitidos."""
    ...


def calcular_monto_reserva(reserva_id: int) -> float:
    """Calcula el monto total que debe pagarse por una reserva."""
    ...    
