"""Menú de Administrador - Interfaz de Usuario por Consola

Interfaz para funciones administrativas del sistema.
Solo accesible para usuarios con rol 'administrador'.
"""
from src.dto.usuario_dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_OPCION_INVALIDA,
    limpiar_pantalla,
    pausar,
    validar_opcion,
)


def mostrar_menu_admin(usuario: UsuarioDTO):
    """Muestra el menú principal de administrador."""
    while True:
        limpiar_pantalla()
        print(f"=== VIAJES AVENTURA - ADMIN: {usuario.nombre} ===")
        print("1. Destinos")
        print("2. Actividades")
        print("3. Paquetes")
        print("4. Reportes")
        print("5. Cerrar Sesión")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if int(opcion) == 1:
            menu_admin_destinos()
        elif int(opcion) == 2:
            menu_admin_actividades()
        elif int(opcion) == 3:
            menu_admin_paquetes()
        elif int(opcion) == 4:
            menu_admin_reportes()
        elif int(opcion) == 5:
            break


def menu_admin_destinos():
    """Submenú para gestión de destinos."""
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: DESTINOS ===")
        print("1. Listar Destinos")
        print("2. Agregar Destino")
        print("3. Editar Destino")
        print("4. Eliminar Destino")
        print("5. Volver")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: LISTAR DESTINOS ===")
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR DESTINO ===")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR DESTINO ===")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR DESTINO ===")
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_actividades():
    """Submenú para gestión de actividades."""
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: ACTIVIDADES ===")
        print("1. Listar Actividades")
        print("2. Agregar Actividad")
        print("3. Editar Actividad")
        print("4. Eliminar Actividad")
        print("5. Volver")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: LISTAR ACTIVIDADES ===")
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR ACTIVIDAD ===")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR ACTIVIDAD ===")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR ACTIVIDAD ===")
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_paquetes():
    """Submenú para gestión de paquetes."""
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: PAQUETES ===")
        print("1. Listar Paquetes")
        print("2. Agregar Paquete")
        print("3. Editar Paquete")
        print("4. Eliminar Paquete")
        print("5. Volver")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: LISTAR PAQUETES ===")
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR PAQUETE ===")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR PAQUETE ===")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR PAQUETE ===")
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_reportes():
    """Submenú para reportes administrativos."""
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: REPORTES ===")
        print("1. Ver todas las Reservas")
        print("2. Reporte de Ventas")
        print("3. Reporte de Clientes")
        print("4. Volver")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 4):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: TODAS LAS RESERVAS ===")
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: REPORTE DE VENTAS ===")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: REPORTE DE CLIENTES ===")
            pausar()
        elif int(opcion) == 4:
            break