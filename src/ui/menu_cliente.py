'''Menú de Cliente - Interfaz de Usuario por Consola

Interfaz para funciones del cliente en el sistema.
Accesible para usuarios con rol 'cliente'.'''

from src.business.pago_manager import obtener_historial_pagos, procesar_pago
from src.business.reserva_manager import (
    cancelar_reserva as cancelar_reserva_manager,
)
from src.business.reserva_manager import crear_reserva as crear_reserva_manager
from src.business.reserva_manager import (
    crear_reserva_destino as crear_reserva_destino_manager,
)
from src.dao.destino_dao import DestinoDAO
from src.dao.paquete_dao import PaqueteDAO
from src.dao.reserva_dao import ReservaDAO
from src.dao.usuario_dao import UsuarioDAO
from src.dto.usuario_dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_OPCION_INVALIDA,
    OperacionCancelada,
    limpiar_pantalla,
    pausar,
    validar_cancelacion,
    validar_opcion,
)
from src.utils.constants import METODOS_PAGO
from src.utils.utils import (
    mostrar_actividades_paquete,
    mostrar_tabla_destinos,
    mostrar_tabla_pagos,
    mostrar_tabla_paquetes,
    mostrar_tabla_reservas,
)


def mostrar_menu_cliente(usuario: UsuarioDTO):
    """Muestra el menú principal de cliente."""
    while True:
        limpiar_pantalla()
        print(f"=== VIAJES AVENTURA - CLIENTE: {usuario.nombre} ===")
        print("1. Ver Destinos Disponibles")
        print("2. Ver Paquetes Disponibles")
        print("3. Crear Reserva de Paquete")
        print("4. Crear Reserva de Destino")
        print("5. Mis Reservas")
        print("6. Realizar Pago")
        print("7. Historial de Pagos")
        print("8. Mi Perfil")
        print("9. Cerrar Sesión")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 9):
            print(MSG_ERROR_OPCION_INVALIDA)
            continue
        if int(opcion) == 1:
            ver_destinos_disponibles()
        elif int(opcion) == 2:
            ver_paquetes_disponibles()
        elif int(opcion) == 3:
            crear_reserva(usuario.id)  # type: ignore
        elif int(opcion) == 4:
            crear_reserva_destino(usuario.id)  # type: ignore
        elif int(opcion) == 5:
            ver_mis_reservas(usuario.id)  # type: ignore
        elif int(opcion) == 6:
            realizar_pago_cliente(usuario.id)  # type: ignore
        elif int(opcion) == 7:
            ver_mis_pagos(usuario.id)  # type: ignore
        elif int(opcion) == 8:
            # Pasar el objeto usuario completo y actualizar si cambia
            usuario_actualizado = ver_mi_perfil(usuario)
            if usuario_actualizado:
                usuario = usuario_actualizado
        elif int(opcion) == 9:
            break


def ver_destinos_disponibles():
    """Lista todos los destinos disponibles."""
    destino_dao = DestinoDAO()
    limpiar_pantalla()
    print("=== DESTINOS DISPONIBLES ===\n")
    
    try:
        destinos = destino_dao.listar_todos()
        if not destinos:
            print("No hay destinos disponibles en este momento.")
        else:
            mostrar_tabla_destinos(destinos)
    except Exception as e:
        print(f"ERROR: Error al cargar destinos: {e}")
    pausar()


def ver_paquetes_disponibles():
    """Lista paquetes con cupos disponibles y sus actividades."""
    paquete_dao = PaqueteDAO()
    limpiar_pantalla()
    print("=== PAQUETES DISPONIBLES ===\n")
    
    try:
        paquetes = paquete_dao.listar_disponibles()
        if not paquetes:
            print("No hay paquetes disponibles en este momento.")
        else:
            # Mostrar cada paquete con sus actividades
            for paquete in paquetes:
                precio = f"${int(paquete.precio_total):,}".replace(",", ".")
                fecha_inicio = str(paquete.fecha_inicio)[:16] if paquete.fecha_inicio else "N/A"
                fecha_fin = str(paquete.fecha_fin)[:16] if paquete.fecha_fin else "N/A"
                
                print("\n" + "="*100)
                print(f"ID: {paquete.id}")
                print(f"NOMBRE: {paquete.nombre}")
                print(f"PRECIO: {precio}")
                print(f"CUPOS DISPONIBLES: {paquete.cupos_disponibles}")
                print(f"INICIO: {fecha_inicio}")
                print(f"FIN: {fecha_fin}")
                print(f"DESCRIPCIÓN: {paquete.descripcion or 'Sin descripción'}")
                
                # Mostrar actividades incluidas
                actividades = paquete_dao.obtener_actividades_paquete(paquete.id)
                mostrar_actividades_paquete(actividades)
            print("="*100 + "\n")
    except Exception as e:
        print(f"ERROR: Error al cargar paquetes: {e}")
    pausar()


def crear_reserva(cliente_id: int):
    """Proceso de creación de nueva reserva."""
    paquete_dao = PaqueteDAO()
    limpiar_pantalla()
    print("=== CREAR RESERVA ===")
    print("(Presione Enter, '0' o 'cancelar' en cualquier momento para abortar)\n")
    
    try:
        # Mostrar paquetes disponibles
        paquetes = paquete_dao.listar_disponibles()
        if not paquetes:
            print("No hay paquetes disponibles.")
            pausar()
            return
        
        print("Paquetes disponibles:")
        mostrar_tabla_paquetes(paquetes)
        
        # Solicitar datos con validación de cancelación
        paquete_id_str = validar_cancelacion(input("\nID del paquete: "))
        paquete_id = int(paquete_id_str)
        
        # Obtener el paquete seleccionado y validar cupos
        paquete_seleccionado = paquete_dao.obtener_por_id(paquete_id)
        if not paquete_seleccionado:
            print("ERROR: El paquete seleccionado no existe.")
            pausar()
            return
        
        num_personas_str = validar_cancelacion(input("Número de personas: "))
        num_personas = int(num_personas_str)
        
        # Validar cupos disponibles
        if num_personas > paquete_seleccionado.cupos_disponibles:
            print("\nERROR: No hay suficientes cupos disponibles.")
            print(f"Cupos disponibles: {paquete_seleccionado.cupos_disponibles}")
            print(f"Personas solicitadas: {num_personas}")
            print(f"Por favor, ingrese un número menor o igual a {paquete_seleccionado.cupos_disponibles}")
            pausar()
            return
        
        # Mostrar resumen antes de confirmar
        print("\n=== RESUMEN DE LA RESERVA ===")
        print(f"Paquete: {paquete_seleccionado.nombre}")
        print(f"Fecha inicio: {paquete_seleccionado.fecha_inicio}")
        print(f"Fecha fin: {paquete_seleccionado.fecha_fin}")
        print(f"Número de personas: {num_personas}")
        print(f"Precio por persona: ${int(paquete_seleccionado.precio_total):,}".replace(",", "."))
        print(f"Monto total: ${int(paquete_seleccionado.precio_total * num_personas):,}".replace(",", "."))
        
        confirmacion = input("\n¿Confirmar reserva? (s/n): ")
        if confirmacion.lower() != 's':
            print("Reserva cancelada.")
            pausar()
            return
        
        # Crear reserva usando el manager
        reserva_id = crear_reserva_manager(cliente_id, paquete_id, num_personas)
        print(f"\nEXITO: Reserva creada exitosamente con ID: {reserva_id}")
        print("Estado: Pendiente de pago")
        print("\nPuedes realizar el pago desde el menú 'Realizar Pago'")
        
    except OperacionCancelada:
        print("\nINFO: Operación cancelada.")
        
    except ValueError as e:
        print(f"ERROR: Error en los datos: {e}")
    except Exception as e:
        print(f"ERROR: Error al crear reserva: {e}")
    pausar()


def crear_reserva_destino(cliente_id: int):
    """Proceso de creación de reserva de destino individual."""
    destino_dao = DestinoDAO()
    limpiar_pantalla()
    print("=== CREAR RESERVA DE DESTINO ===")
    print("(Presione Enter, '0' o 'cancelar' en cualquier momento para abortar)\n")
    
    try:
        # Mostrar destinos disponibles
        destinos = destino_dao.listar_todos()
        if not destinos:
            print("No hay destinos disponibles.")
            pausar()
            return
        
        print("Destinos disponibles:")
        mostrar_tabla_destinos(destinos)
        
        # Solicitar datos con validación de cancelación
        destino_id_str = validar_cancelacion(input("\nID del destino: "))
        destino_id = int(destino_id_str)
        
        # Obtener el destino seleccionado y validar cupos
        destino_seleccionado = destino_dao.obtener_por_id(destino_id)
        if not destino_seleccionado:
            print("ERROR: El destino seleccionado no existe.")
            pausar()
            return
        
        num_personas_str = validar_cancelacion(input("Número de personas: "))
        num_personas = int(num_personas_str)
        
        # Validar cupos disponibles
        if num_personas > destino_seleccionado.cupos_disponibles:
            print("\nERROR: No hay suficientes cupos disponibles.")
            print(f"Cupos disponibles: {destino_seleccionado.cupos_disponibles}")
            print(f"Personas solicitadas: {num_personas}")
            print(f"Por favor, ingrese un número menor o igual a {destino_seleccionado.cupos_disponibles}")
            pausar()
            return
        
        # Mostrar resumen antes de confirmar
        print("\n=== RESUMEN DE LA RESERVA ===")
        print(f"Destino: {destino_seleccionado.nombre}")
        print(f"Descripción: {destino_seleccionado.descripcion}")
        print(f"Número de personas: {num_personas}")
        print(f"Costo por persona: ${int(destino_seleccionado.costo_base):,}".replace(",", "."))
        print(f"Monto total: ${int(destino_seleccionado.costo_base * num_personas):,}".replace(",", "."))
        
        confirmacion = input("\n¿Confirmar reserva? (s/n): ")
        if confirmacion.lower() != 's':
            print("Reserva cancelada.")
            pausar()
            return
        
        # Crear reserva usando el manager
        reserva_id = crear_reserva_destino_manager(cliente_id, destino_id, num_personas)
        print(f"\nEXITO: Reserva de destino creada exitosamente con ID: {reserva_id}")
        print("Estado: Pendiente de pago")
        print("\nPuedes realizar el pago desde el menú 'Realizar Pago'")
        
    except OperacionCancelada:
        print("\nINFO: Operación cancelada.")
        
    except ValueError as e:
        print(f"ERROR: Error en los datos: {e}")
    except Exception as e:
        print(f"ERROR: Error al crear reserva de destino: {e}")
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
            mostrar_tabla_reservas(reservas)
            
            # Opciones adicionales
            print("\nOpciones:")
            print("1. Cancelar una reserva")
            print("2. Volver")
            opcion = input("Seleccione: ")
            if opcion == "1":
                cancelar_reserva(cliente_id)
    except Exception as e:
        print(f"ERROR: Error al cargar reservas: {e}")
    pausar()


def cancelar_reserva(cliente_id: int):
    """Proceso de cancelación de reserva."""
    reserva_dao = ReservaDAO()
    
    try:
        reserva_id = int(input("\nID de la reserva a cancelar: "))
        
        # Verificar que la reserva pertenece al cliente
        reserva = reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            print("ERROR: Reserva no encontrada")
            pausar()
            return
        
        if reserva.usuario_id != cliente_id:
            print("ERROR: Esta reserva no te pertenece")
            pausar()
            return
        
        if reserva.estado == "CANCELADA":
            print("ERROR: Esta reserva ya está cancelada")
            pausar()
            return
        
        confirmacion = input(f"¿Confirma cancelación de reserva {reserva_id}? (s/n): ")
        if confirmacion.lower() == 's':
            if cancelar_reserva_manager(reserva_id):
                print("EXITO: Reserva cancelada exitosamente")
                print("Los cupos han sido devueltos al paquete")
            else:
                print("ERROR: No se pudo cancelar la reserva")
        pausar()
    except Exception as e:
        print(f"ERROR: Error: {e}")
        pausar()


def realizar_pago_cliente(cliente_id: int):
    """Proceso de pago de una reserva."""
    reserva_dao = ReservaDAO()
    limpiar_pantalla()
    print("=== REALIZAR PAGO ===\n")
    
    try:
        # Mostrar reservas pendientes de pago
        reservas = reserva_dao.listar_por_cliente(cliente_id)
        reservas_pendientes = [r for r in reservas if r.estado in ["PENDIENTE", "CONFIRMADA"]]
        
        if not reservas_pendientes:
            print("No tienes reservas pendientes de pago.")
            pausar()
            return
        
        print("Reservas pendientes de pago:")
        for r in reservas_pendientes:
            print(f"  [{r.id}] Paquete {r.paquete_id} - ${int(r.monto_total):,} - {r.numero_personas} personas - Estado: {r.estado}".replace(",", "."))
        
        reserva_id = int(input("\nID de la reserva a pagar: "))
        
        # Verificar que la reserva existe y pertenece al cliente
        reserva = reserva_dao.obtener_por_id(reserva_id)
        if not reserva or reserva.usuario_id != cliente_id:
            print("ERROR: Reserva no válida")
            pausar()
            return
        
        if reserva.estado not in ["PENDIENTE", "CONFIRMADA"]:
            print("ERROR: No se puede pagar esta reserva.")
            print(f"Estado actual: {reserva.estado}")
            if reserva.estado == "PAGADA":
                print("Esta reserva ya fue pagada.")
            elif reserva.estado == "CANCELADA":
                print("Esta reserva está cancelada.")
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
        
        print(f"\nMonto a pagar: ${int(reserva.monto_total):,}".replace(",", "."))
        confirmacion = input("¿Confirmar pago? (s/n): ")
        
        if confirmacion.lower() == 's':
            pago_id = procesar_pago(reserva_id, metodo_pago)
            print("\nEXITO: Pago procesado exitosamente")
            print(f"ID de pago: {pago_id}")
            print(f"Método: {metodo_pago}")
            print("La reserva ha sido marcada como 'Pagada'")
        else:
            print("Pago cancelado")
            
    except Exception as e:
        print(f"ERROR: Error al procesar pago: {e}")
    pausar()


def ver_mis_pagos(cliente_id: int):
    """Historial de pagos."""
    reserva_dao = ReservaDAO()
    limpiar_pantalla()
    print("=== HISTORIAL DE PAGOS ===\n")
    
    try:
        # Obtener todas las reservas del cliente
        reservas = reserva_dao.listar_por_cliente(cliente_id)
        
        todos_pagos = []
        for reserva in reservas:
            pagos = obtener_historial_pagos(reserva.id)
            if pagos:
                todos_pagos.extend(pagos)
        
        if not todos_pagos:
            print("No tienes pagos registrados.")
        else:
            mostrar_tabla_pagos(todos_pagos)
            
    except Exception as e:
        print(f"ERROR: Error al cargar pagos: {e}")
    pausar()


def ver_mi_perfil(usuario: UsuarioDTO) -> UsuarioDTO | None:
    """Muestra información del cliente y permite editarlo. Retorna usuario actualizado si cambia."""
    usuario_dao = UsuarioDAO()
    limpiar_pantalla()
    print("=== MI PERFIL ===\n")
    
    try:
        # Recargar datos actuales del usuario
        usuario_actual = usuario_dao.obtener_por_id(usuario.id)  # type: ignore
        if not usuario_actual:
            print("ERROR: Error al cargar perfil")
            pausar()
            return None
        
        print(f"Nombre: {usuario_actual.nombre}")
        print(f"Email: {usuario_actual.email}")
        print(f"Rol: {usuario_actual.rol}")
        print(f"Fecha de registro: {usuario_actual.fecha_registro}")
        
        print("\n1. Editar perfil")
        print("2. Volver")
        opcion = input("Seleccione: ")
        if opcion == "1":
            usuario_modificado = actualizar_perfil(usuario_actual)
            pausar()
            return usuario_modificado
        else:
            return None
            
    except Exception as e:
        print(f"ERROR: Error: {e}")
        pausar()
        return None


def actualizar_perfil(usuario: UsuarioDTO) -> UsuarioDTO | None:
    """Modificar datos del usuario. Retorna usuario actualizado o None si falla."""
    usuario_dao = UsuarioDAO()
    
    try:
        print("\n=== EDITAR PERFIL ===")
        nuevo_nombre = input(f"Nuevo nombre (Enter='{usuario.nombre}'): ") or usuario.nombre
        nuevo_email = input(f"Nuevo email (Enter='{usuario.email}'): ") or usuario.email
        
        usuario.nombre = nuevo_nombre
        usuario.email = nuevo_email
        
        if usuario_dao.actualizar(usuario):
            print("EXITO: Perfil actualizado exitosamente")
            return usuario
        else:
            print("ERROR: No se pudo actualizar el perfil")
            return None
            
    except Exception as e:
        print(f"ERROR: Error: {e}")
        return None