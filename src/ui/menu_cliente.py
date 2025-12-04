'''Menú de Cliente - Interfaz de Usuario por Consola

Interfaz para funciones del cliente en el sistema.
Accesible para usuarios con rol 'cliente'.'''

from src.business.pago_manager import obtener_historial_pagos, procesar_pago
from src.business.reserva_manager import (
    cancelar_reserva as cancelar_reserva_manager,
)
from src.business.reserva_manager import crear_reserva as crear_reserva_manager
from src.dao.paquete_dao import PaqueteDAO
from src.dao.reserva_dao import ReservaDAO
from src.dao.usuario_dao import UsuarioDAO
from src.dto.usuario_dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_OPCION_INVALIDA,
    limpiar_pantalla,
    pausar,
    validar_opcion,
)
from src.utils.constants import METODOS_PAGO


def mostrar_menu_cliente(usuario: UsuarioDTO):
    """Muestra el menú principal de cliente."""
    while True:
        limpiar_pantalla()
        print(f"=== VIAJES AVENTURA - CLIENTE: {usuario.nombre} ===")
        print("1. Ver Paquetes Disponibles")
        print("2. Crear Reserva")
        print("3. Mis Reservas")
        print("4. Realizar Pago")
        print("5. Historial de Pagos")
        print("6. Mi Perfil")
        print("7. Cerrar Sesión")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 7):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if int(opcion) == 1:
            ver_paquetes_disponibles()
        elif int(opcion) == 2:
            crear_reserva(usuario.id)  # type: ignore
        elif int(opcion) == 3:
            ver_mis_reservas(usuario.id)  # type: ignore
        elif int(opcion) == 4:
            realizar_pago_cliente(usuario.id)  # type: ignore
        elif int(opcion) == 5:
            ver_mis_pagos(usuario.id)  # type: ignore
        elif int(opcion) == 6:
            ver_mi_perfil(usuario.id)  # type: ignore
        elif int(opcion) == 7:
            break


def ver_paquetes_disponibles():
    """Lista paquetes con cupos disponibles."""
    paquete_dao = PaqueteDAO()
    limpiar_pantalla()
    print("=== PAQUETES DISPONIBLES ===\n")
    
    try:
        paquetes = paquete_dao.listar_disponibles()
        if not paquetes:
            print("No hay paquetes disponibles en este momento.")
        else:
            for p in paquetes:
                print(f"\n{'='*60}")
                print(f"ID: {p.id} | {p.nombre}")
                print(f"Precio: ${p.precio_total}")
                print(f"Cupos disponibles: {p.cupos_disponibles}")
                print(f"Fechas: {p.fecha_inicio} al {p.fecha_fin}")
                print(f"{'='*60}")
    except Exception as e:
        print(f"✗ Error al cargar paquetes: {e}")
    pausar()


def crear_reserva(cliente_id: int):
    """Proceso de creación de nueva reserva."""
    paquete_dao = PaqueteDAO()
    limpiar_pantalla()
    print("=== CREAR RESERVA ===\n")
    
    try:
        # Mostrar paquetes disponibles
        paquetes = paquete_dao.listar_disponibles()
        if not paquetes:
            print("No hay paquetes disponibles.")
            pausar()
            return
        
        print("Paquetes disponibles:")
        for p in paquetes:
            print(f"  [{p.id}] {p.nombre} - ${p.precio_total} - {p.cupos_disponibles} cupos")
        
        # Solicitar datos
        paquete_id = int(input("\nID del paquete: "))
        num_personas = int(input("Número de personas: "))
        fecha_viaje = input("Fecha de viaje (YYYY-MM-DD): ")
        
        # Crear reserva usando el manager
        reserva_id = crear_reserva_manager(cliente_id, paquete_id, num_personas, fecha_viaje)
        print(f"\n✓ Reserva creada exitosamente con ID: {reserva_id}")
        print("Estado: Pendiente")
        print("Siguiente paso: Confirmar reserva y realizar pago")
        
    except ValueError as e:
        print(f"✗ Error en los datos: {e}")
    except Exception as e:
        print(f"✗ Error al crear reserva: {e}")
    pausar()


def ver_mis_reservas(cliente_id: int):
    """Lista reservas del cliente."""
    reserva_dao = ReservaDAO()
    limpiar_pantalla()
    print("=== MIS RESERVAS ===\n")
    
    try:
        reservas = reserva_dao.listar_por_cliente(cliente_id)
        if not reservas:
            print("No tienes reservas registradas.")
        else:
            for r in reservas:
                print(f"\n{'-'*60}")
                print(f"ID Reserva: {r.id}")
                print(f"Paquete ID: {r.paquete_id}")
                print(f"Estado: {r.estado}")
                print(f"Personas: {r.numero_personas}")
                print(f"Monto Total: ${r.monto_total}")
                print(f"Fecha Reserva: {r.fecha_reserva}")
                print(f"{'-'*60}")
            
            # Opciones adicionales
            print("\nOpciones:")
            print("1. Cancelar una reserva")
            print("2. Volver")
            opcion = input("Seleccione: ")
            if opcion == "1":
                cancelar_reserva(cliente_id)
    except Exception as e:
        print(f"✗ Error al cargar reservas: {e}")
    pausar()


def cancelar_reserva(cliente_id: int):
    """Proceso de cancelación de reserva."""
    reserva_dao = ReservaDAO()
    
    try:
        reserva_id = int(input("\nID de la reserva a cancelar: "))
        
        # Verificar que la reserva pertenece al cliente
        reserva = reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            print("✗ Reserva no encontrada")
            pausar()
            return
        
        if reserva.usuario_id != cliente_id:
            print("✗ Esta reserva no te pertenece")
            pausar()
            return
        
        if reserva.estado == "CANCELADA":
            print("✗ Esta reserva ya está cancelada")
            pausar()
            return
        
        confirmacion = input(f"¿Confirma cancelación de reserva {reserva_id}? (s/n): ")
        if confirmacion.lower() == 's':
            if cancelar_reserva_manager(reserva_id):
                print("✓ Reserva cancelada exitosamente")
                print("Los cupos han sido devueltos al paquete")
            else:
                print("✗ No se pudo cancelar la reserva")
    except Exception as e:
        print(f"✗ Error: {e}")
    pausar()


def realizar_pago_cliente(cliente_id: int):
    """Proceso de pago de una reserva."""
    reserva_dao = ReservaDAO()
    limpiar_pantalla()
    print("=== REALIZAR PAGO ===\n")
    
    try:
        # Mostrar reservas confirmadas pendientes de pago
        reservas = reserva_dao.listar_por_cliente(cliente_id)
        reservas_pendientes = [r for r in reservas if r.estado == "CONFIRMADA"]
        
        if not reservas_pendientes:
            print("No tienes reservas confirmadas pendientes de pago.")
            pausar()
            return
        
        print("Reservas pendientes de pago:")
        for r in reservas_pendientes:
            print(f"  [{r.id}] Paquete {r.paquete_id} - ${r.monto_total} - {r.numero_personas} personas")
        
        reserva_id = int(input("\nID de la reserva a pagar: "))
        
        # Verificar que la reserva existe y pertenece al cliente
        reserva = reserva_dao.obtener_por_id(reserva_id)
        if not reserva or reserva.usuario_id != cliente_id:
            print("✗ Reserva no válida")
            pausar()
            return
        
        if reserva.estado != "CONFIRMADA":
            print(f"✗ La reserva debe estar en estado 'CONFIRMADA'. Estado actual: {reserva.estado}")
            pausar()
            return
        
        # Seleccionar método de pago
        print("\nMétodos de pago disponibles:")
        for i, metodo in enumerate(METODOS_PAGO, 1):
            print(f"  {i}. {metodo}")
        
        metodo_opcion = int(input("Seleccione método de pago: "))
        if not validar_opcion(metodo_opcion, 1, len(METODOS_PAGO)):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            return
        metodo_pago = METODOS_PAGO[metodo_opcion - 1]
        
        print(f"\nMonto a pagar: ${reserva.monto_total}")
        confirmacion = input("¿Confirmar pago? (s/n): ")
        
        if confirmacion.lower() == 's':
            pago_id = procesar_pago(reserva_id, metodo_pago)
            print("\n✓ Pago procesado exitosamente")
            print(f"ID de pago: {pago_id}")
            print(f"Método: {metodo_pago}")
            print("La reserva ha sido marcada como 'Pagada'")
        else:
            print("Pago cancelado")
            
    except Exception as e:
        print(f"✗ Error al procesar pago: {e}")
    pausar()


def ver_mis_pagos(cliente_id: int):
    """Historial de pagos."""
    reserva_dao = ReservaDAO()
    limpiar_pantalla()
    print("=== HISTORIAL DE PAGOS ===\n")
    
    try:
        # Obtener todas las reservas del cliente
        reservas = reserva_dao.listar_por_cliente(cliente_id)
        
        pagos_encontrados = False
        for reserva in reservas:
            pagos = obtener_historial_pagos(reserva.id)
            if pagos:
                pagos_encontrados = True
                print(f"\nReserva ID: {reserva.id}")
                for p in pagos:
                    print(f"  Pago ID: {p.id}")
                    print(f"  Monto: ${p.monto}")
                    print(f"  Método: {p.metodo}")
                    print(f"  Estado: {p.estado}")
                    print(f"  Fecha: {p.fecha_pago}")
                    print(f"  {'-'*50}")
        
        if not pagos_encontrados:
            print("No tienes pagos registrados.")
            
    except Exception as e:
        print(f"✗ Error al cargar pagos: {e}")
    pausar()


def ver_mi_perfil(cliente_id: int):
    """Muestra información del cliente."""
    usuario_dao = UsuarioDAO()
    limpiar_pantalla()
    print("=== MI PERFIL ===\n")
    
    try:
        usuario = usuario_dao.obtener_por_id(cliente_id)
        if not usuario:
            print("✗ Error al cargar perfil")
            pausar()
            return
        
        print(f"Nombre: {usuario.nombre}")
        print(f"Email: {usuario.email}")
        print(f"Rol: {usuario.rol}")
        print(f"Fecha de registro: {usuario.fecha_registro}")
        
        print("\n1. Editar perfil")
        print("2. Volver")
        opcion = input("Seleccione: ")
        if opcion == "1":
            actualizar_perfil(cliente_id)
            
    except Exception as e:
        print(f"✗ Error: {e}")
    pausar()


def actualizar_perfil(cliente_id: int):
    """Modificar datos del usuario."""
    usuario_dao = UsuarioDAO()
    
    try:
        usuario = usuario_dao.obtener_por_id(cliente_id)
        if not usuario:
            print("✗ Usuario no encontrado")
            return
        
        print("\n=== EDITAR PERFIL ===")
        nuevo_nombre = input(f"Nuevo nombre (Enter='{usuario.nombre}'): ") or usuario.nombre
        nuevo_email = input(f"Nuevo email (Enter='{usuario.email}'): ") or usuario.email
        
        usuario.nombre = nuevo_nombre
        usuario.email = nuevo_email
        
        if usuario_dao.actualizar(usuario):
            print("✓ Perfil actualizado exitosamente")
        else:
            print("✗ No se pudo actualizar el perfil")
            
    except Exception as e:
        print(f"✗ Error: {e}")
    pausar()