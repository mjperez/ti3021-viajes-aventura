'''Menú de Cliente - Interfaz de Usuario por Consola

Interfaz para funciones del cliente en el sistema.
Accesible para usuarios con rol 'cliente'.'''

from src.business.actividad_service import ActividadService
from src.business.destino_service import DestinoService
from src.business.pago_service import PagoService
from src.business.paquete_service import PaqueteService
from src.business.reserva_service import ReservaService
from src.business.usuario_service import UsuarioService
from src.dto.usuario_dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_OPCION_INVALIDA,
    OperacionCancelada,
    leer_opcion,
    limpiar_pantalla,
    pausar,
    validar_cancelacion,
    validar_opcion,
)
from src.utils.constants import METODOS_PAGO
from src.utils.utils import (
    mostrar_actividades_paquete,
    mostrar_tabla_actividades,
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
        print("3. Ver Políticas de Cancelación")
        print("4. Crear Reserva de Paquete")
        print("5. Crear Reserva de Destino")
        print("6. Mis Reservas")
        print("7. Realizar Pago")
        print("8. Historial de Pagos")
        print("9. Mi Perfil")
        print("10. Cerrar Sesión")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 10):
            print(MSG_ERROR_OPCION_INVALIDA)
            continue
        if opcion == 1:
            ver_destinos_disponibles()
        elif opcion == 2:
            ver_paquetes_disponibles()
        elif opcion == 3:
            ver_politicas_cancelacion_cliente()
        elif opcion == 4:
            crear_reserva(usuario.id)  # type: ignore
        elif opcion == 5:
            crear_reserva_destino(usuario.id)  # type: ignore
        elif opcion == 6:
            ver_mis_reservas(usuario.id)  # type: ignore
        elif opcion == 7:
            realizar_pago_cliente(usuario.id)  # type: ignore
        elif opcion == 8:
            ver_mis_pagos(usuario.id)  # type: ignore
        elif opcion == 9:
            # Pasar el objeto usuario completo y actualizar si cambia
            usuario_actualizado = ver_mi_perfil(usuario)
            if usuario_actualizado:
                usuario = usuario_actualizado
        elif opcion == 10:
            break


def ver_actividades_disponibles():
    """Lista todas las actividades disponibles o filtra por destino."""
    actividad_service = ActividadService()
    destino_service = DestinoService()
    limpiar_pantalla()
    print("=== ACTIVIDADES DISPONIBLES ===\n")
    
    try:
        print("1. Ver todas las actividades")
        print("2. Buscar por destino")
        print("3. Volver")
        opcion = input("\nSeleccione una opción: ")
        
        if opcion == "2":
            limpiar_pantalla()
            destinos = destino_service.listar_destinos_disponibles()
            if not destinos:
                print("\nNo hay destinos disponibles.")
            else:
                print("\nDestinos disponibles:")
                for d in destinos:
                    print(f"  ID {d.id}: {d.nombre}")
                
                destino_id_str = input("\nIngrese ID del destino (0 para cancelar): ")
                destino_id = int(destino_id_str)
                
                if destino_id > 0:
                    limpiar_pantalla()
                    actividades = actividad_service.listar_actividades_por_destino(destino_id)
                    if not actividades:
                        print("\nNo hay actividades disponibles para ese destino.")
                    else:
                        print("\nActividades del destino seleccionado:")
                        mostrar_tabla_actividades(actividades, con_iva=True)
        elif opcion == "1":
            limpiar_pantalla()
            actividades = actividad_service.listar_todas_actividades()
            if not actividades:
                print("\nNo hay actividades disponibles en este momento.")
            else:
                mostrar_tabla_actividades(actividades, con_iva=True)
    except ValueError:
        print("\nERROR: Debe ingresar un numero valido")
    except Exception as e:
        print(f"\nERROR: Error al cargar actividades: {e}")
    pausar()


def ver_destinos_disponibles():
    """Lista todos los destinos disponibles."""
    destino_service = DestinoService()
    limpiar_pantalla()
    print("=== DESTINOS DISPONIBLES ===\n")
    
    try:
        destinos = destino_service.listar_destinos_disponibles()
        if not destinos:
            print("No hay destinos disponibles en este momento.")
        else:
            mostrar_tabla_destinos(destinos, con_iva=True)
    except Exception as e:
        print(f"ERROR: Error al cargar destinos: {e}")
    pausar()


def ver_paquetes_disponibles():
    """Lista paquetes con cupos disponibles y sus actividades."""

    paquete_service = PaqueteService()

    limpiar_pantalla()
    print("=== PAQUETES DISPONIBLES ===\n")
    
    try:
        paquetes = paquete_service.listar_paquetes_disponibles()
        if not paquetes:
            print("No hay paquetes disponibles en este momento.")
        else:
            mostrar_tabla_paquetes(paquetes, con_iva=True)
            

    except Exception as e:
        print(f"ERROR: Error al cargar paquetes: {e}")
    pausar()


def crear_reserva(cliente_id: int):
    """Proceso de creación de nueva reserva."""
    paquete_service = PaqueteService()
    limpiar_pantalla()
    print("=== CREAR RESERVA ===")
    print("(Escriba 'cancelar' para abortar)\n")
    
    try:
        # Mostrar paquetes disponibles
        paquetes = paquete_service.listar_paquetes_disponibles()
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
        paquete_seleccionado = paquete_service.obtener_paquete(paquete_id)
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
        from src.dao.paquete_actividad_dao import PaqueteActividadDAO
        paquete_actividad_dao = PaqueteActividadDAO()
        
        print("\n=== RESUMEN DE LA RESERVA ===")
        print(f"Paquete: {paquete_seleccionado.nombre}")
        print(f"Fecha inicio: {paquete_seleccionado.fecha_inicio}")
        print(f"Fecha fin: {paquete_seleccionado.fecha_fin}")
        
        # Mostrar actividades incluidas
        actividades = paquete_actividad_dao.listar_actividades_por_paquete(paquete_id)
        if actividades:
            print("\nActividades incluidas:")
            for a in actividades:
                print(f"  • {a['nombre']}")
        
        print(f"\nNúmero de personas: {num_personas}")
        print(f"Precio por persona: ${int(paquete_seleccionado.precio_total):,}".replace(",", "."))
        print(f"Monto total: ${int(paquete_seleccionado.precio_total * num_personas):,}".replace(",", "."))
        
        confirmacion = input("\n¿Confirmar reserva? (s/n): ")
        if confirmacion.lower() != 's':
            print("Reserva cancelada.")
            pausar()
            return
        
        # Crear reserva usando el service
        reserva_service = ReservaService()
        reserva_id = reserva_service.crear_reserva_paquete(cliente_id, paquete_id, num_personas)
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
    destino_service = DestinoService()
    limpiar_pantalla()
    print("=== CREAR RESERVA DE DESTINO ===")
    print("(Escriba 'cancelar' para abortar)\n")
    
    try:
        # Mostrar destinos disponibles
        destinos = destino_service.listar_destinos_disponibles()
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
        destino_seleccionado = destino_service.obtener_destino(destino_id)
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
        
        # Crear reserva usando el service
        reserva_service = ReservaService()
        reserva_id = reserva_service.crear_reserva_destino(cliente_id, destino_id, num_personas)
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
    reserva_service = ReservaService()
    limpiar_pantalla()
    print("=== MIS RESERVAS ===\n")
    
    try:
        reservas = reserva_service.listar_reservas_cliente(cliente_id)
        if not reservas:
            print("No tienes reservas registradas.")
        else:
            mostrar_tabla_reservas(reservas, mostrar_cliente=False)
            
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
    """Proceso de cancelación de reserva con aplicación de política de reembolso."""
    reserva_service = ReservaService()
    
    try:
        reserva_id = int(input("\nID de la reserva a cancelar: "))
        
        # Verificar que la reserva pertenece al cliente
        reserva = reserva_service.obtener_reserva(reserva_id)
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
        
        if reserva.estado == "COMPLETADA":
            print("ERROR: No se puede cancelar una reserva ya completada")
            pausar()
            return
        
        # Informar al cliente sobre el estado
        print(f"\nEstado actual de la reserva: {reserva.estado}")
        if reserva.estado in ["PAGADA", "CONFIRMADA"]:
            print("NOTA: Se aplicará la política de cancelación para determinar el reembolso.")
        
        confirmacion = input(f"\n¿Confirma cancelación de reserva {reserva_id}? (s/n): ")
        if confirmacion.lower() == 's':
            resultado = reserva_service.cancelar_reserva(reserva_id)
            if resultado["cancelada"]:
                print("\n✓ ÉXITO: Reserva cancelada exitosamente")
                print("Los cupos han sido devueltos")
            else:
                print(f"ERROR: {resultado['mensaje']}")
        pausar()
    except Exception as e:
        print(f"ERROR: {e}")
        pausar()


def realizar_pago_cliente(cliente_id: int):
    """Proceso de pago de una reserva."""
    reserva_service = ReservaService()
    limpiar_pantalla()
    print("=== REALIZAR PAGO ===\n")
    
    try:
        # Mostrar reservas pendientes de pago
        reservas = reserva_service.listar_reservas_cliente(cliente_id)
        reservas_pendientes = [r for r in reservas if r.estado in ["PENDIENTE", "CONFIRMADA"]]
        
        if not reservas_pendientes:
            print("No tienes reservas pendientes de pago.")
            pausar()
            return
        
        print("Reservas pendientes de pago:")
        for r in reservas_pendientes:
            # Determinar si es paquete o destino
            tipo = "Paquete" if r.paquete_id else "Destino"
            id_ref = r.paquete_id if r.paquete_id else r.destino_id
            print(f"  [{r.id}] {tipo} #{id_ref} - ${int(r.monto_total):,} - {r.numero_personas} personas - Estado: {r.estado}".replace(",", "."))
        
        reserva_id = int(input("\nID de la reserva a pagar: "))
        
        # Verificar que la reserva existe y pertenece al cliente
        reserva = reserva_service.obtener_reserva(reserva_id)
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
            pago_service = PagoService()
            pago_id = pago_service.procesar_pago(reserva_id, metodo_pago)
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
    reserva_service = ReservaService()
    limpiar_pantalla()
    print("=== HISTORIAL DE PAGOS ===\n")
    
    try:
        # Obtener todas las reservas del cliente
        reservas = reserva_service.listar_reservas_cliente(cliente_id)
        
        pago_service = PagoService()
        todos_pagos = []
        for reserva in reservas:
            if reserva.id is not None:  # Validar que id no sea None
                pagos = pago_service.obtener_historial_pagos(reserva.id)
                if pagos:
                    todos_pagos.extend(pagos)
        
        if not todos_pagos:
            print("No tienes pagos registrados.")
        else:
            mostrar_tabla_pagos(todos_pagos)
            
    except Exception as e:
        print(f"ERROR: Error al cargar pagos: {e}")
    pausar()


def ver_politicas_cancelacion_cliente():
    """Muestra las políticas de cancelación disponibles para clientes."""
    from src.business.politica_cancelacion_service import PoliticaCancelacionService
    
    politica_service = PoliticaCancelacionService()
    
    limpiar_pantalla()
    print("=== POLÍTICAS DE CANCELACIÓN ===\n")
    
    try:
        politicas = politica_service.listar_todas_politicas()
        if not politicas:
            print("No hay políticas de cancelación registradas.")
        else:
            print("="*100)
            print(f"{'ID':<5} {'NOMBRE':<30} {'DÍAS DE AVISO':<20} {'% REEMBOLSO':<20}")
            print("="*100)
            for p in politicas:
                print(f"{p.id:<5} {p.nombre:<30} {p.dias_aviso:<20} {p.porcentaje_reembolso}%")
            print("="*100)
            print("\n📋 Estas políticas aplican a las reservas de PAQUETES y DESTINOS.")
            print("   El reembolso depende de cuándo canceles tu reserva.")
            print("\n   • Flexible: Puedes cancelar hasta 3 días antes y recibir reembolso completo.")
            print("   • Estricta: Debes cancelar con al menos 7 días de anticipación para 50% de reembolso.")
    except Exception as e:
        print(f"ERROR: Error al cargar políticas: {e}")
    pausar()


def ver_mi_perfil(usuario: UsuarioDTO) -> UsuarioDTO | None:
    """Muestra información del cliente y permite editarlo. Retorna usuario actualizado si cambia."""
    usuario_service = UsuarioService()
    limpiar_pantalla()
    print("=== MI PERFIL ===\n")
    
    try:
        # Recargar datos actuales del usuario
        usuario_actual = usuario_service.obtener_usuario(usuario.id)  # type: ignore
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
    usuario_service = UsuarioService()
    
    try:
        print("\n=== EDITAR PERFIL ===")
        nuevo_nombre = input(f"Nuevo nombre (Enter='{usuario.nombre}'): ") or usuario.nombre
        
        # Actualizar usando el servicio
        usuario_actualizado = usuario_service.actualizar_perfil(
            usuario.id,  # type: ignore
            nuevo_nombre
        )
        
        print("\nEXITO: Perfil actualizado correctamente")
        pausar()
        return usuario_actualizado
            
    except Exception as e:
        print(f"ERROR: Error: {e}")
        pausar()
        return None