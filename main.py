"""Sistema de Reservas - Viajes Aventura

Punto de entrada principal de la aplicación.
Inicia la interfaz de usuario por consola.

Curso: TI3021 - Programación Orientada a Objetos Seguro
Arquitectura: Patrones DAO/DTO
Base de Datos: MySQL
Integrantes: Maria Jesus Perez, Maria Isabel Rubio

Ejecución:
    python main.py
"""

from src.config.db_connection import cerrar_conexion, obtener_conexion
from src.ui.menu_principal import opcion_login, opcion_registro
from src.utils import (
    MSG_ERROR_OPCION_INVALIDA,
    leer_opcion,
    limpiar_pantalla,
    pausar,
    validar_opcion,
)


def verificar_conexion_bd():
    """Verifica que la conexión a la base de datos esté disponible."""
    try:
        conn = obtener_conexion()
        if conn:
            print("Conexión a base de datos exitosa")
            return True
        else:
            print("No se pudo conectar a la base de datos")
            return False
    except Exception as e:
        print(f"Error al conectar con la base de datos: {e}")
        return False


def mostrar_banner():
    """Muestra el banner de bienvenida de la aplicación."""
    print("="*60)
    print("           SISTEMA DE RESERVAS - VIAJES AVENTURA")
    print("="*60)
    print("")


def main():
    """Función principal del programa."""
    try:
        # Verificar conexión a BD al inicio
        limpiar_pantalla()
        mostrar_banner()
        print("Verificando conexión a la base de datos...")
        
        if not verificar_conexion_bd():
            print("\nNo se puede iniciar la aplicación sin conexión a BD.")
            print("Verifique que MySQL esté ejecutándose y las credenciales sean correctas.")
            pausar()
            return
        
        pausar()
        
        # Loop principal del menú
        while True:
            limpiar_pantalla()
            mostrar_banner()
            print("1. Iniciar Sesión")
            print("2. Registrarse")
            print("3. Salir")
            print("")
            opcion = leer_opcion()
            
            if not validar_opcion(opcion, 1, 3):
                print(MSG_ERROR_OPCION_INVALIDA)
                pausar()
                continue
            
            if opcion == 1:
                opcion_login()
            elif opcion == 2:
                opcion_registro()
            elif opcion == 3:
                limpiar_pantalla()
                print("\n" + "="*60)
                print("   Gracias por usar Viajes Aventura. ¡Hasta luego!")
                print("="*60 + "\n")
                break
    
    except KeyboardInterrupt:
        print("\n\nInterrupción detectada. Cerrando aplicación...")
    except Exception as e:
        print(f"\nError crítico: {e}")
        print("La aplicación se cerrará.")
    finally:
        # Cerrar conexiones al finalizar
        try:
            cerrar_conexion()
            print("Conexiones cerradas correctamente.")
        except Exception as e:
            print(f"Error al cerrar las conexiones: {e}")


if __name__ == "__main__":
    main()