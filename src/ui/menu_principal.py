'''
Menú Principal - Interfaz de Usuario por Consola

Punto de entrada principal para la interfaz de usuario.
Muestra opciones de login, registro y navegación.

Navegación:
    1. Login → redirige a menu_cliente o menu_admin según rol
    2. Registro → crea nuevo cliente
    3. Salir
'''
from src.business.auth_manager import (
    login,
    registrar_usuario,
)
from src.dto.usuario_dto import UsuarioDTO
from src.ui.menu_admin import mostrar_menu_admin
from src.ui.menu_cliente import mostrar_menu_cliente
from src.utils import (
    leer_opcion,
    limpiar_pantalla,
    pausar,
)


def mostrar_menu_principal(usuario: UsuarioDTO): 
    '''Redirige al menú correspondiente según el rol del usuario.'''
    if usuario.rol == 'ADMIN':
        mostrar_menu_admin(usuario)
    elif usuario.rol == 'CLIENTE':
        mostrar_menu_cliente(usuario)

def opcion_login(): 
    '''Maneja el proceso de login'''
    limpiar_pantalla()
    print("=== VIAJES AVENTURA: LOGIN ===")
    email = input("Ingrese su email: ")
    password = input("Ingrese su contraseña: ")
    try:
        usuario = login(email,password)
        if usuario:
            print(f"¡Bienvenido, {usuario.nombre}!")
            pausar()
            mostrar_menu_principal(usuario)
        else:
            print("Credenciales inválidas. Intente nuevamente.")
            pausar()
    except Exception as e:
        print(f"Error durante el login: {str(e)}")
        pausar()
    
def opcion_registro(): 
    '''Maneja el proceso de registro de cliente'''
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: REGISTRO ===")
        nombre = input("Ingrese su nombre: ")
        rut = input("Ingrese su RUT (ej: 12.345.678-9): ")
        email = input("Ingrese su email: ")
        password = input("Ingrese su contraseña: ")
        
        try:
            usuario = registrar_usuario(rut, email, password, nombre)
            print(f"¡Registro exitoso! Bienvenido, {usuario.nombre}. Ahora puede iniciar sesión.")
            pausar()
            break  # Salir del loop si el registro fue exitoso
            
        except Exception as e:
            print(f"\nError durante el registro: {str(e)}")
            print("\n1. Intentar nuevamente")
            print("2. Volver al menú principal")
            opcion = leer_opcion()
            
            if opcion != "1":
                break  # Salir si el usuario no quiere reintentar