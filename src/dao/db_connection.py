"""Módulo de Conexión a Base de Datos

Gestiona la conexión a la base de datos MySQL.
Implementa patrón Singleton para reutilizar la conexión.

Funciones esperadas:
    - obtener_conexion(): Retorna una conexión a MySQL
    - cerrar_conexion(): Cierra la conexión activa
    - ejecutar_query(query, params): Ejecuta una consulta SELECT
    - ejecutar_insert(query, params): Ejecuta INSERT y retorna el ID generado
    - ejecutar_update(query, params): Ejecuta UPDATE/DELETE
    - iniciar_transaccion(): Inicia una transacción
    - commit(): Confirma los cambios
    - rollback(): Revierte los cambios

Usa variables de entorno desde config.settings para:
    - DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD
"""