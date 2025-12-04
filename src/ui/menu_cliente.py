'''Menú de Cliente - Interfaz de Usuario por Consola

Interfaz para funciones del cliente en el sistema.
Accesible para usuarios con rol 'cliente'.'''

from src.dto.usuario_dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_OPCION_INVALIDA,
    limpiar_pantalla,
    pausar,
    validar_opcion,
)


def mostrar_menu_cliente(usuario: UsuarioDTO):
    """Muestra el menú principal de cliente."""
    while True:
        limpiar_pantalla()
        print(f"=== VIAJES AVENTURA - CLIENTE: {usuario.nombre} ===")
        print("1. Ver Paquetes Disponibles")
        print("2. Mis Reservas")
        print("3. Realizar Pago")
        print("4. Historial de Pagos")
        print("5. Mi Perfil")
        print("6. Cerrar Sesión")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 6):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if int(opcion) == 1:
            ver_paquetes_disponibles()
        elif int(opcion) == 2:
            ver_mis_reservas(usuario.id)  # type: ignore
        elif int(opcion) == 3:
            realizar_pago(usuario.id)  # type: ignore
        elif int(opcion) == 4:
            ver_mis_pagos(usuario.id)  # type: ignore
        elif int(opcion) == 5:
            ver_mi_perfil(usuario.id)  # type: ignore
        elif int(opcion) == 6:
            break

    
def ver_paquetes_disponibles(): 
    #Lista paquetes con cupos disponibles
    ...
def ver_detalle_paquete(paquete_id:int): 
    #Muestra información completa del paquete
    ...
def crear_reserva(): 
    #Proceso de creación de nueva reserva
    ...
def ver_mis_reservas(cliente_id:int): 
    #Lista reservas del cliente
    ...
def cancelar_reserva(reserva_id:int): 
    #Proceso de cancelación de reserva
    ...
def realizar_pago(reserva_id:int): 
    #Proceso de pago de una reserva
    ...
def ver_mis_pagos(cliente_id:int): 
    #Historial de pagos
    ...
def ver_mi_perfil(cliente_id:int):
    #Muestra información del cliente
    ...
def actualizar_perfil(cliente_id:int): 
    #Modificar datos del usuario
    ...