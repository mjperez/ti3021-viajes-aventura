"""DTO para Pago - Data Transfer Object

Clase que representa los datos de un pago.

Atributos esperados:
    - id: int
    - reserva_id: int (FK a Reservas)
    - monto: decimal
    - fecha_pago: datetime
    - metodo: string ('efectivo', 'tarjeta_credito', 'tarjeta_debito', 'transferencia')
    - estado: string ('pendiente', 'completado', 'fallido', 'reembolsado')
    - referencia: string
"""