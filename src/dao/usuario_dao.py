"""DAO para Usuario - Data Access Object

Maneja todas las operaciones de base de datos relacionadas con Usuarios.
Implementa operaciones CRUD.

Métodos esperados:
    - crear(usuario_dto): Inserta un nuevo usuario
    - obtener_por_id(id): Busca usuario por ID
    - obtener_por_email(email): Busca usuario por email (para login)
    - actualizar(id, usuario_dto): Actualiza datos del usuario
    - eliminar(id): Elimina un usuario (soft delete recomendado)
    - listar_todos(): Retorna lista de todos los usuarios
    - listar_por_rol(rol): Retorna usuarios filtrados por rol
    - verificar_email_existe(email): Valida si el email ya está registrado
"""