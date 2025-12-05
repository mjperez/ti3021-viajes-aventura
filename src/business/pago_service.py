"""Service Layer para Pagos

Encapsula la lógica de negocio relacionada con pagos.
Intermediario entre la UI y el DAO para mantener separación de capas.
Reemplaza completamente a pago_manager.py (eliminando redundancia).
"""

from src.dao.pago_dao import PagoDAO
from src.dao.reserva_dao import ReservaDAO
from src.dto.pago_dto import PagoDTO
from src.utils.constants import METODOS_PAGO
from src.utils.exceptions import ValidacionError


class PagoService:
    """Servicio para gestión de pagos."""
    
    def __init__(self):
        """Inicializa el servicio con sus DAOs."""
        self.pago_dao = PagoDAO()
        self.reserva_dao = ReservaDAO()
    
    def procesar_pago(self, reserva_id: int, metodo_pago: str) -> int:
        """Procesa un pago completado y marca la reserva como pagada.
        
        Args:
            reserva_id: ID de la reserva
            metodo_pago: Método de pago (EFECTIVO, TARJETA, TRANSFERENCIA)
            
        Returns:
            ID del pago creado
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        if metodo_pago not in METODOS_PAGO:
            raise ValidacionError(f"Método de pago inválido. Métodos válidos: {', '.join(METODOS_PAGO)}")
        
        # Obtener la reserva
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError("La reserva no existe")
        
        # Verificar que la reserva esté pendiente o confirmada
        if reserva.estado not in ["PENDIENTE", "CONFIRMADA"]:
            raise ValidacionError(f"La reserva debe estar PENDIENTE o CONFIRMADA. Estado actual: {reserva.estado}")
        
        # Calcular monto
        monto = reserva.monto_total
        
        # Registrar el pago
        pago_id = self.pago_dao.registrar_pago_completado(reserva_id, monto, metodo_pago)
        
        # Marcar la reserva como pagada
        self.reserva_dao.marcar_como_pagada(reserva_id)
        
        return pago_id
    
    def verificar_estado_pago(self, reserva_id: int) -> bool:
        """Verifica si existe un pago completado para la reserva.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            True si hay un pago completado
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        pagos = self.pago_dao.obtener_por_reserva(reserva_id)
        
        # Verificar si hay algún pago completado
        for pago in pagos:
            if pago.estado == "COMPLETADO":
                return True
        
        return False
    
    def obtener_historial_pagos(self, reserva_id: int) -> list[PagoDTO]:
        """Retorna el historial de todos los pagos de una reserva.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            Lista de PagoDTO de la reserva
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        return self.pago_dao.obtener_por_reserva(reserva_id)
    
    def generar_reporte_ventas(self, fecha_inicio: str, fecha_fin: str) -> dict:
        """Genera un reporte de ventas con total y listado de pagos en un periodo.
        
        Args:
            fecha_inicio: Fecha de inicio del período (formato: YYYY-MM-DD)
            fecha_fin: Fecha de fin del período (formato: YYYY-MM-DD)
            
        Returns:
            Diccionario con datos del reporte
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if not fecha_inicio or not fecha_fin:
            raise ValidacionError("Las fechas de inicio y fin son requeridas")
        
        # Obtener total del periodo
        total = self.pago_dao.obtener_total_por_periodo(fecha_inicio, fecha_fin)
        
        # Obtener listado de pagos
        pagos = self.pago_dao.listar_por_fecha(fecha_inicio, fecha_fin)
        
        return {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'total': total or 0,
            'cantidad_pagos': len(pagos),
            'pagos': pagos
        }
    
    def calcular_monto_reserva(self, reserva_id: int) -> float:
        """Calcula el monto total que debe pagarse por una reserva.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            Monto total de la reserva
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError("La reserva no existe")
        
        return reserva.monto_total
