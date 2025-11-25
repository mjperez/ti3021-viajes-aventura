"""DTO para Usuario - Data Transfer Object

Clase que representa los datos de un usuario del sistema.
Utilizada para transferir información entre capas sin lógica de negocio.

Atributos esperados:
    - id: int
    - email: string
    - password_hash: string
    - nombre: string
    - rol: string ('cliente' o 'administrador')
    - fecha_registro: datetime
"""