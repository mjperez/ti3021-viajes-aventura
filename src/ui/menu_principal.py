"""Menú Principal - Interfaz de Usuario por Consola

Punto de entrada principal para la interfaz de usuario.
Muestra opciones de login, registro y navegación.

Funciones esperadas:
    - mostrar_menu_principal(): Muestra menú inicial
    - opcion_login(): Maneja el proceso de login
    - opcion_registro(): Maneja el proceso de registro de cliente
    - validar_opcion(opcion, min, max): Valida entrada del usuario
    - limpiar_pantalla(): Limpia la consola
    - pausar(): Espera input del usuario antes de continuar

Navegación:
    1. Login → redirige a menu_cliente o menu_admin según rol
    2. Registro → crea nuevo cliente
    3. Salir
"""