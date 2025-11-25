"""DAO para Reserva - Data Access Object

Maneja todas las operaciones de base de datos relacionadas con Reservas.

Métodos esperados:
    - crear(reserva_dto): Inserta una nueva reserva en estado 'pendiente'
    - obtener_por_id(id): Busca reserva por ID con JOINs a cliente y paquete
    - actualizar(id, reserva_dto): Actualiza datos de la reserva
    - cambiar_estado(id, nuevo_estado): Cambia el estado de la reserva
    - listar_por_cliente(cliente_id): Retorna reservas de un cliente
    - listar_por_paquete(paquete_id): Retorna reservas de un paquete
    - listar_por_estado(estado): Retorna reservas filtradas por estado
    - confirmar(id): Cambia estado a 'confirmada'
    - marcar_como_pagada(id): Cambia estado a 'pagada'
    - cancelar(id): Cambia estado a 'cancelada' y restaura cupos
"""