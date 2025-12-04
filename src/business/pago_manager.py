"""Gestor de Pagos - Business Logic"""

from src.dao.pago_dao import PagoDAO
from src.dao.reserva_dao import ReservaDAO
from src.dto.pago_dto import PagoDTO
from src.utils.constants import ESTADOS_PAGO, METODOS_PAGO


def procesar_pago(reserva_id: int, metodo_pago: str) -> int:
    """Procesa un pago completado y marca la reserva como pagada."""
    pago_dao = PagoDAO()
    reserva_dao = ReservaDAO()
    
    # Validar método de pago
    if not validar_metodo_pago(metodo_pago):
        raise ValueError(f"Método de pago inválido. Métodos válidos: {', '.join(METODOS_PAGO)}")
    
    # Obtener la reserva
    reserva = reserva_dao.obtener_por_id(reserva_id)
    if not reserva:
        raise ValueError("La reserva no existe")
    
    # Verificar que la reserva esté confirmada
    if reserva.estado != "Confirmada":
        raise ValueError(f"La reserva debe estar Confirmada. Estado actual: {reserva.estado}")
    
    # Calcular monto
    monto = reserva.monto_total
    
    # Registrar el pago
    pago_id = pago_dao.registrar_pago_completado(reserva_id, monto, metodo_pago)
    
    # Marcar la reserva como pagada
    reserva_dao.marcar_como_pagada(reserva_id)
    
    return pago_id


def verificar_estado_pago(reserva_id: int) -> bool:
    """Verifica si existe un pago completado para la reserva."""
    pago_dao = PagoDAO()
    
    pagos = pago_dao.obtener_por_reserva(reserva_id)
    
    # Verificar si hay algún pago completado
    for pago in pagos:
        if pago.estado == ESTADOS_PAGO[1]:  # "Completado"
            return True
    
    return False


def obtener_historial_pagos(reserva_id: int) -> list[PagoDTO]:
    """Retorna el historial de todos los pagos de una reserva."""
    pago_dao = PagoDAO()
    return pago_dao.obtener_por_reserva(reserva_id)


def generar_reporte_ventas(fecha_inicio: str, fecha_fin: str) -> dict:
    """Genera un reporte de ventas con total y listado de pagos en un periodo."""
    pago_dao = PagoDAO()
    
    # Obtener total del periodo
    total = pago_dao.obtener_total_por_periodo(fecha_inicio, fecha_fin)
    
    # Obtener listado de pagos
    pagos = pago_dao.listar_por_fecha(fecha_inicio, fecha_fin)
    
    return {
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total': total,
        'cantidad_pagos': len(pagos),
        'pagos': pagos
    }


def validar_metodo_pago(metodo: str) -> bool:
    """Valida que el método de pago sea uno de los permitidos."""
    return metodo in METODOS_PAGO


def calcular_monto_reserva(reserva_id: int) -> float:
    """Calcula el monto total que debe pagarse por una reserva."""
    reserva_dao = ReservaDAO()
    
    reserva = reserva_dao.obtener_por_id(reserva_id)
    if not reserva:
        raise ValueError("La reserva no existe")
    
    return reserva.monto_total
