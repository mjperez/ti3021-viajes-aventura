'''Menú de Cliente - Interfaz de Usuario por Consola

Interfaz para funciones del cliente en el sistema.
Accesible para usuarios con rol 'cliente'.'''

from utils.utils import limpiar_pantalla, pausar, validar_opcion


def mostrar_menu_cliente(usuario):
    cliente_id = 0
    reserva_id = 0
    print("--- Menú Cliente---\n" \
    "\t1. Ver Paquetes Disponibles\n" \
    "\t2. Mis Reservas\n" \
    "\t. Realizar Pago\n" \
    "\t4. Historial de Pagos\n" \
    "\t5. Mi Perfil\n" \
    "\t6. Cerrar Sesión\n")
    opcion = input("Elija su opción: ")
    opcion_int = int(opcion)
    if opcion_int == 1:
        ver_paquetes_disponibles()
        paquete_id = input("Elija que paquete desea revisar: ")
        paquete_id_int = int(paquete_id)
        ver_detalle_paquete(paquete_id_int)
    elif opcion_int == 2:
        ver_mis_reservas(cliente_id)
    elif opcion_int == 3:
        realizar_pago(reserva_id)
    elif opcion_int == 4:
        ver_mis_pagos(cliente_id)
    elif opcion_int == 5:
        ver_mi_perfil(cliente_id)
    elif opcion_int == 6:
        ...

    
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