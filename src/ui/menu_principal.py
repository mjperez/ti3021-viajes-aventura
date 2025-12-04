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
    MSG_ERROR_OPCION_INVALIDA,
    limpiar_pantalla,
    pausar,
    validar_opcion,
)


def mostrar_menu_principal(usuario: UsuarioDTO): 
    """Redirige al menú correspondiente según el rol del usuario."""
    if usuario.rol == 'admin':
        mostrar_menu_admin(usuario)
    elif usuario.rol == 'cliente':
        mostrar_menu_cliente(usuario)

def opcion_login(): 
    #Maneja el proceso de login
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
    #Maneja el proceso de registro de cliente
    limpiar_pantalla()
    print("=== VIAJES AVENTURA: REGISTRO ===")
    nombre = input("Ingrese su nombre: ")
    email = input("Ingrese su email: ")
    password = input("Ingrese su contraseña: ")
    try:
        usuario = registrar_usuario(email,password,nombre)
        print(f"¡Registro exitoso! Bienvenido, {usuario.nombre}. Ahora puede iniciar sesión.")
        pausar()
    except Exception as e:
        print(f"Error durante el registro: {str(e)}")
        pausar()



if __name__ == "__main__":
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA ===")
        print("1. Login")
        print("2. Registro")
        print("3. Salir")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion),1,3):
            print(MSG_ERROR_OPCION_INVALIDA)
        elif int(opcion) == 1:
            opcion_login()
        elif int(opcion) == 2:
            opcion_registro()
        elif int(opcion) == 3:
            print("Gracias por usar Viajes Aventura. ¡Hasta luego!")
            break