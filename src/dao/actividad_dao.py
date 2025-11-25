"""DAO para Actividad - Data Access Object

Maneja todas las operaciones de base de datos relacionadas con Actividades.

Métodos esperados:
    - crear(actividad_dto): Inserta una nueva actividad
    - obtener_por_id(id): Busca actividad por ID
    - actualizar(id, actividad_dto): Actualiza datos de la actividad
    - eliminar(id): Elimina una actividad
    - listar_todas(): Retorna lista de todas las actividades
    - listar_por_destino(destino_id): Retorna actividades de un destino específico
"""