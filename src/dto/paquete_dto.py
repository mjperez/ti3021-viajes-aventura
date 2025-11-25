"""DTO para Paquete - Data Transfer Object

Clase que representa los datos de un paquete turístico.

Atributos esperados:
    - id: int
    - nombre: string
    - descripcion: string
    - precio_total: decimal
    - duracion_dias: int
    - cupos_disponibles: int
    - fecha_inicio: date
    - fecha_fin: date
    - politica_cancelacion_id: int (FK)
"""