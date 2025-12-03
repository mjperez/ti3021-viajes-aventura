"""Gestor de Pagos - Business Logic

Maneja toda la lógica de negocio relacionada con pagos.
Coordina el procesamiento de pagos y actualización de estados.

Funciones esperadas:
    - procesar_pago(reserva_id, monto, metodo): Procesa un pago y actualiza reserva
    - validar_monto(reserva_id, monto): Valida que el monto coincida con la reserva
    - registrar_pago_exitoso(reserva_id, monto, metodo, referencia): Registra pago completado
    - procesar_reembolso(pago_id): Procesa un reembolso
    - obtener_historial_pagos(reserva_id): Retorna historial de pagos de una reserva
    - generar_referencia_pago(): Genera código único de referencia
    - validar_metodo_pago(metodo): Valida que el método sea permitido

Requiere:
    - pago_dao, reserva_dao
    - Manejo de transacciones para consistencia
"""

from src.dao import PagoDAO, ReservaDAO
