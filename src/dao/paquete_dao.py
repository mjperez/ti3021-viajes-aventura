"""DAO para Paquete - Data Access Object

Maneja todas las operaciones de base de datos relacionadas con Paquetes.

Métodos esperados:
    - crear(paquete_dto): Inserta un nuevo paquete
    - obtener_por_id(id): Busca paquete por ID con JOIN a destinos y política
    - actualizar(id, paquete_dto): Actualiza datos del paquete
    - eliminar(id): Elimina un paquete
    - listar_todos(): Retorna lista de todos los paquetes
    - listar_disponibles(): Retorna paquetes con cupos > 0
    - reducir_cupo(id): Decrementa cupos_disponibles
    - aumentar_cupo(id): Incrementa cupos_disponibles
    - agregar_destino(paquete_id, destino_id): Asocia destino al paquete
    - eliminar_destino(paquete_id, destino_id): Desasocia destino del paquete
"""