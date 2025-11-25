"""DAO para Destino - Data Access Object

Maneja todas las operaciones de base de datos relacionadas con Destinos.

Métodos esperados:
    - crear(destino_dto): Inserta un nuevo destino
    - obtener_por_id(id): Busca destino por ID
    - actualizar(id, destino_dto): Actualiza datos del destino
    - eliminar(id): Elimina un destino
    - listar_todos(): Retorna lista de todos los destinos
    - buscar_por_nombre(nombre): Busca destinos por nombre (LIKE)
"""