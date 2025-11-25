"""DAO para Pago - Data Access Object

Maneja todas las operaciones de base de datos relacionadas con Pagos.

Métodos esperados:
    - crear(pago_dto): Inserta un nuevo pago
    - obtener_por_id(id): Busca pago por ID
    - obtener_por_reserva(reserva_id): Retorna pagos de una reserva
    - actualizar_estado(id, nuevo_estado): Cambia el estado del pago
    - registrar_pago_completado(reserva_id, monto, metodo): Procesa un pago exitoso
    - listar_por_fecha(fecha_inicio, fecha_fin): Retorna pagos en rango de fechas
    - obtener_total_por_periodo(fecha_inicio, fecha_fin): Suma montos de pagos completados
"""