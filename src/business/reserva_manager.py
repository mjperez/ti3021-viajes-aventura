"""Gestor de Reservas - Business Logic

Maneja toda la lógica de negocio relacionada con reservas.
Coordina operaciones entre múltiples DAOs.

Funciones esperadas:
    - crear_reserva(cliente_id, paquete_id, numero_personas): Crea reserva y reduce cupos
    - confirmar_reserva(reserva_id): Confirma una reserva pendiente
    - cancelar_reserva(reserva_id): Cancela reserva y aplica política de cancelación
    - calcular_monto_total(paquete_id, numero_personas): Calcula monto total
    - verificar_disponibilidad(paquete_id, numero_personas): Valida cupos disponibles
    - obtener_reservas_cliente(cliente_id): Lista reservas del cliente
    - aplicar_politica_cancelacion(reserva_id): Calcula reembolso según política
    - validar_fechas_reserva(paquete_id): Valida que el paquete esté en fechas válidas

Requiere:
    - reserva_dao, paquete_dao
    - Manejo de transacciones para integridad de datos
"""