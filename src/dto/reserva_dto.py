"""DTO para Reserva - Data Transfer Object

Clase que representa los datos de una reserva.

Atributos esperados:
    - id: int
    - cliente_id: int (FK a Usuarios)
    - paquete_id: int (FK a Paquetes)
    - fecha_reserva: datetime
    - estado: string ('pendiente', 'confirmada', 'pagada', 'cancelada')
    - numero_personas: int
    - monto_total: decimal
"""