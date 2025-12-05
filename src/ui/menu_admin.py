"""Men� de Administrador - Interfaz de Usuario por Consola

Interfaz para funciones administrativas del sistema.
Solo accesible para usuarios con rol 'administrador'.
"""
from datetime import datetime

from src.business.actividad_service import ActividadService
from src.business.destino_service import DestinoService
from src.business.paquete_service import PaqueteService
from src.business.reserva_service import ReservaService
from src.business.usuario_service import UsuarioService
from src.dto import UsuarioDTO
from src.utils import (
    MSG_ERROR_OPCION_INVALIDA,
    OperacionCancelada,
    limpiar_pantalla,
    pausar,
    validar_cancelacion,
    validar_opcion,
)
from src.utils.utils import (
    mostrar_tabla_actividades,
    mostrar_tabla_destinos,
    mostrar_tabla_paquetes,
    mostrar_tabla_reservas,
)


def mostrar_menu_admin(usuario: UsuarioDTO):
    """Muestra el men� principal de administrador."""
    while True:
        limpiar_pantalla()
        print(f"=== VIAJES AVENTURA - ADMIN: {usuario.nombre} ===")
        print("1. Destinos")
        print("2. Actividades")
        print("3. Paquetes")
        print("4. Políticas de Cancelación")
        print("5. Reportes")
        print("6. Cerrar Sesión")
        opcion = input("Elija su opción: ")
        if not validar_opcion(int(opcion), 1, 6):
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
            menu_admin_politicas()
        elif int(opcion) == 5:
            menu_admin_reportes()
        elif int(opcion) == 6:
            break


def menu_admin_destinos():
    """Submen� para gesti�n de destinos."""
    destino_service = DestinoService()
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: DESTINOS ===")
        print("1. Listar Destinos")
        print("2. Agregar Destino")
        print("3. Editar Destino")
        print("4. Eliminar Destino")
        print("5. Volver")
        opcion = input("Elija su opci�n: ")
        
        if not validar_opcion(int(opcion), 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: LISTAR DESTINOS ===")
            dest = input("Ingrese nombre de destino a buscar (o Enter para todos): ")
            if dest:
                print(f"Mostrando destinos que coinciden con '{dest}'...")
                destinos = destino_service.buscar_destinos_por_nombre(dest)
                mostrar_tabla_destinos(destinos)
            else:
                print("Mostrando todos los destinos...")
                destinos = destino_service.listar_todos_destinos()
                mostrar_tabla_destinos(destinos)
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR DESTINO ===")
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
            try:
                nombre = validar_cancelacion(input("Nombre del destino: "))
                descripcion = validar_cancelacion(input("Descripci�n: "))
                costo_base_str = validar_cancelacion(input("Costo base del destino: "))
                costo_base = float(costo_base_str)
                cupos_str = validar_cancelacion(input("Cupos disponibles (Enter=50): ")) or "50"
                cupos = int(cupos_str)
                
                print(f"Agregando destino '{nombre}'...")
                new_destino = destino_service.crear_destino(nombre, "Pa�s", descripcion, costo_base, cupos)
                print(f"EXITO: Destino '{nombre}' agregado con ID: {new_destino.id}")
            except OperacionCancelada:
                print("\nINFO: Operaci�n cancelada.")
            except Exception as e:
                print(f"ERROR: Error al agregar destino: {e}")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR DESTINO ===")
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
            try:
                destinos = destino_service.listar_todos_destinos()
                print("Destinos disponibles:")
                for d in destinos:
                    print(f"- {d.nombre} (ID: {d.id})")
                    
                id_editar_str = validar_cancelacion(input("\nIngrese el ID del destino a editar: "))
                id_editar = int(id_editar_str)
                
                destino = destino_service.obtener_destino(id_editar)
                if not destino:
                    print(f"ERROR: No se encontr� destino con ID {id_editar}.")
                    pausar()
                    continue
                    
                print(f"\nDestino a editar: {destino.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (Enter para mantener '{destino.nombre}'): ") or destino.nombre
                nueva_descripcion = input("Nueva descripci�n (Enter para mantener): ") or destino.descripcion
                nuevo_costo_base_str = input(f"Nuevo costo base (Enter para mantener '{destino.costo_base}'): ")
                nuevo_costo_base = float(nuevo_costo_base_str) if nuevo_costo_base_str else destino.costo_base
                nuevos_cupos_str = input(f"Nuevos cupos (Enter para mantener '{destino.cupos_disponibles}'): ")
                nuevos_cupos = int(nuevos_cupos_str) if nuevos_cupos_str else destino.cupos_disponibles
                
                print(f"\nActualizando destino ID {id_editar}...")
                destino_actualizado = destino_service.actualizar_destino(
                    id_editar,
                    nuevo_nombre,
                    "Pa�s",  # Campo pais no disponible en la entrada original
                    nueva_descripcion,
                    nuevo_costo_base,
                    nuevos_cupos
                )
                print(f"EXITO: Destino '{destino_actualizado.nombre}' actualizado correctamente.")
            except OperacionCancelada:
                print("\nINFO: Operaci�n cancelada.")
            except Exception as e:
                print(f"ERROR: Error al editar destino: {e}")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR DESTINO ===")
            destinos = destino_service.listar_todos_destinos()
            print("Destinos disponibles:")
            for d in destinos:
                print(f"- {d.nombre} (ID: {d.id})")
            id_eliminar = int(input("\nIngrese el ID del destino a eliminar: "))
            destino = destino_service.obtener_destino(id_eliminar)
            if not destino:
                print(f"No se encontr� destino con ID {id_eliminar}.")
                pausar()
                continue
            print(f"Destino a eliminar: {destino.nombre}")
            confirmar = input("�Est� seguro? (s/n): ")
            if confirmar.lower() != 's':    
                print("Eliminaci�n cancelada.")
                pausar()
                continue
            print(f"Eliminando destino ID {id_eliminar}...")
            # Lógica para eliminar destino
            try:
                eliminado = destino_service.eliminar_destino(id_eliminar)
                if eliminado:
                    print(f"Destino ID {id_eliminar} eliminado exitosamente.")
                else:
                    print(f"No se pudo eliminar el destino ID {id_eliminar}.")
            except Exception as e:
                print(f"Error al eliminar destino: {e}")
      
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_actividades():
    """Submen� para gesti�n de actividades."""
    actividad_service = ActividadService()
    destino_service = DestinoService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: ACTIVIDADES ===")
        print("1. Listar Actividades")
        print("2. Agregar Actividad")
        print("3. Editar Actividad")
        print("4. Eliminar Actividad")
        print("5. Volver")
        opcion = input("Elija su opci�n: ")
        if not validar_opcion(int(opcion), 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: LISTAR ACTIVIDADES ===")
            actividades = actividad_service.listar_todas_actividades()
            if not actividades:
                print("No hay actividades registradas.")
            else:
                mostrar_tabla_actividades(actividades)
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR ACTIVIDAD ===")
            # Listar destinos disponibles
            destinos = destino_service.listar_todos_destinos()
            if not destinos:
                print("No hay destinos disponibles. Cree destinos primero.")
                pausar()
                continue
            print("\nDestinos disponibles:")
            for d in destinos:
                print(f"  ID: {d.id} - {d.nombre}")
            
            try:
                nombre = input("\nNombre de la actividad: ")
                descripcion = input("Descripci�n: ")
                duracion = int(input("Duraci�n (horas): "))
                precio = float(input("Precio base: "))
                destino_id = int(input("ID del destino: "))
                
                nueva_actividad = actividad_service.crear_actividad(nombre, descripcion, duracion, precio, destino_id)
                print(f"EXITO: Actividad creada con ID: {nueva_actividad.id}")
            except Exception as e:
                print(f"ERROR: Error al crear actividad: {e}")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR ACTIVIDAD ===")
            try:
                id_editar = int(input("ID de la actividad a editar: "))
                actividad = actividad_service.obtener_actividad(id_editar)
                if not actividad:
                    print(f"No se encontr� actividad con ID {id_editar}")
                    pausar()
                    continue
                
                print(f"\nActividad actual: {actividad.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (Enter='{actividad.nombre}'): ") or actividad.nombre
                nueva_descripcion = input(f"Nueva descripci�n (Enter='{actividad.descripcion}'): ") or actividad.descripcion
                nueva_duracion = input(f"Nueva duraci�n (Enter={actividad.duracion_horas}h): ")
                nuevo_precio = input(f"Nuevo precio (Enter=${actividad.precio_base}): ")
                nuevo_destino = input(f"Nuevo destino ID (Enter={actividad.destino_id}): ")
                
                actividad.nombre = nuevo_nombre
                actividad.descripcion = nueva_descripcion
                actividad.duracion_horas = int(nueva_duracion) if nueva_duracion else actividad.duracion_horas
                actividad.precio_base = float(nuevo_precio) if nuevo_precio else actividad.precio_base
                actividad.destino_id = int(nuevo_destino) if nuevo_destino else actividad.destino_id
                
                actividad_service.actualizar_actividad(
                    id_editar,
                    actividad.nombre,
                    actividad.descripcion,
                    actividad.duracion_horas,
                    actividad.precio_base,
                    actividad.destino_id
                )
                print("EXITO: Actividad actualizada exitosamente")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR ACTIVIDAD ===")
            try:
                id_eliminar = int(input("ID de la actividad a eliminar: "))
                actividad = actividad_service.obtener_actividad(id_eliminar)
                if not actividad:
                    print(f"No se encontr� actividad con ID {id_eliminar}")
                    pausar()
                    continue
                
                print(f"\nActividad: {actividad.nombre}")
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == 's':
                    if actividad_service.eliminar_actividad(id_eliminar):
                        print("EXITO: Actividad eliminada exitosamente")
                    else:
                        print("ERROR: No se pudo eliminar la actividad")
                else:
                    print("Eliminaci�n cancelada")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_paquetes():
    """Submen� para gesti�n de paquetes."""
    paquete_service = PaqueteService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: PAQUETES ===")
        print("1. Listar Paquetes")
        print("2. Agregar Paquete")
        print("3. Editar Paquete")
        print("4. Eliminar Paquete")
        print("5. Volver")
        opcion = input("Elija su opci�n: ")
        if not validar_opcion(int(opcion), 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: LISTAR PAQUETES ===")
            paquetes = paquete_service.listar_todos_paquetes()
            if not paquetes:
                print("No hay paquetes registrados.")
            else:
                mostrar_tabla_paquetes(paquetes)
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR PAQUETE ===")
            try:
                nombre = input("Nombre del paquete: ")
                fecha_inicio_str = input("Fecha inicio (YYYY-MM-DD): ")
                fecha_fin_str = input("Fecha fin (YYYY-MM-DD): ")
                precio = float(input("Precio total: "))
                cupos = int(input("Cupos disponibles: "))
                politica_id = int(input("ID pol�tica de cancelaci�n (ej: 1): "))
                
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
                
                nuevo_paquete = paquete_service.crear_paquete(
                    nombre,
                    "",  # descripcion
                    fecha_inicio,
                    fecha_fin,
                    precio,
                    cupos,
                    politica_id
                )
                print(f"EXITO: Paquete creado con ID: {nuevo_paquete.id}")
            except Exception as e:
                print(f"ERROR: Error al crear paquete: {e}")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR PAQUETE ===")
            try:
                id_editar = int(input("ID del paquete a editar: "))
                paquete = paquete_service.obtener_paquete(id_editar)
                if not paquete:
                    print(f"No se encontr� paquete con ID {id_editar}")
                    pausar()
                    continue
                
                print(f"\nPaquete actual: {paquete.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (Enter='{paquete.nombre}'): ") or paquete.nombre
                nuevo_precio = input(f"Nuevo precio (Enter=${paquete.precio_total}): ")
                nuevos_cupos = input(f"Nuevos cupos (Enter={paquete.cupos_disponibles}): ")
                
                paquete.nombre = nuevo_nombre
                paquete.precio_total = float(nuevo_precio) if nuevo_precio else paquete.precio_total
                paquete.cupos_disponibles = int(nuevos_cupos) if nuevos_cupos else paquete.cupos_disponibles
                
                paquete_service.actualizar_paquete(
                    id_editar,
                    paquete.nombre,
                    paquete.descripcion or "",
                    paquete.fecha_inicio,
                    paquete.fecha_fin,
                    paquete.precio_total,
                    paquete.cupos_disponibles,
                    paquete.politica_id
                )
                print("EXITO: Paquete actualizado exitosamente")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR PAQUETE ===")
            try:
                id_eliminar = int(input("ID del paquete a eliminar: "))
                paquete = paquete_service.obtener_paquete(id_eliminar)
                if not paquete:
                    print(f"No se encontr� paquete con ID {id_eliminar}")
                    pausar()
                    continue
                
                print(f"\nPaquete: {paquete.nombre}")
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == 's':
                    if paquete_service.eliminar_paquete(id_eliminar):
                        print("EXITO: Paquete eliminado exitosamente")
                    else:
                        print("ERROR: No se pudo eliminar el paquete")
                else:
                    print("Eliminaci�n cancelada")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_reportes():
    """Submenú para reportes administrativos."""
    from src.business.pago_service import PagoService
    from src.utils.constants import ESTADOS_RESERVA
    
    reserva_service = ReservaService()
    usuario_service = UsuarioService()
    pago_service = PagoService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: REPORTES ===")
        print("1. Ver todas las Reservas")
        print("2. Reporte de Ventas")
        print("3. Reporte de Clientes")
        print("4. Volver")
        opcion = input("Elija su opci�n: ")
        if not validar_opcion(int(opcion), 1, 4):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        
        if int(opcion) == 1:
            print("=== VIAJES AVENTURA: TODAS LAS RESERVAS ===")
            print("\nFiltrar por estado:")
            print("0. Todas")
            for i, estado in enumerate(ESTADOS_RESERVA, 1):
                print(f"{i}. {estado}")
            filtro = input("\nSeleccione opci�n (Enter=Todas): ")
            
            try:
                if not filtro or filtro == '0':
                    # Listar todas las reservas
                    todas_reservas = reserva_service.listar_todas_reservas()
                    print(f"\nTotal de reservas: {len(todas_reservas)}")
                    if todas_reservas:
                        mostrar_tabla_reservas(todas_reservas)
                else:
                    estado_seleccionado = ESTADOS_RESERVA[int(filtro) - 1]
                    # Filtrar manualmente por estado
                    todas_reservas = reserva_service.listar_todas_reservas()
                    reservas = [r for r in todas_reservas if r.estado == estado_seleccionado]
                    print(f"\nReservas en estado '{estado_seleccionado}': {len(reservas)}")
                    if reservas:
                        mostrar_tabla_reservas(reservas)
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: REPORTE DE VENTAS ===")
            try:
                fecha_inicio = input("Fecha inicio (YYYY-MM-DD): ")
                fecha_fin = input("Fecha fin (YYYY-MM-DD): ")
                
                reporte = pago_service.generar_reporte_ventas(fecha_inicio, fecha_fin)
                print("\n--- REPORTE DE VENTAS ---")
                print(f"Per�odo: {reporte['fecha_inicio']} al {reporte['fecha_fin']}")
                print(f"Total de pagos: {reporte['cantidad_pagos']}")
                print(f"Monto total: ${reporte['total']:.2f}")
                
                if reporte['pagos']:
                    print("\nDetalle de pagos:")
                    for p in reporte['pagos']:
                        print(f"  ID: {p.id} | Reserva: {p.reserva_id} | ${p.monto} | {p.metodo_pago} | {p.fecha_pago}")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: REPORTE DE CLIENTES ===")
            try:
                todos_usuarios = usuario_service.listar_todos_usuarios()
                clientes = [u for u in todos_usuarios if u.rol == 'cliente']
                print(f"\nTotal de clientes registrados: {len(clientes)}")
                print("\n" + "="*70)
                for c in clientes:
                    print(f"ID: {c.id} | {c.nombre}")
                    print(f"  Email: {c.email}")
                    print(f"  Registro: {c.fecha_registro}")
                    print("-" * 70)
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 4:
            break


def menu_admin_politicas():
    """Submenú para ver políticas de cancelación."""
    from src.business.politica_cancelacion_service import PoliticaCancelacionService
    
    politica_service = PoliticaCancelacionService()
    
    limpiar_pantalla()
    print("=== VIAJES AVENTURA: POLÍTICAS DE CANCELACIÓN ===\n")
    
    try:
        politicas = politica_service.listar_todas_politicas()
        if not politicas:
            print("No hay políticas de cancelación registradas.")
        else:
            print("="*80)
            print(f"{'ID':<5} {'NOMBRE':<20} {'DÍAS AVISO':<15} {'% REEMBOLSO':<15}")
            print("="*80)
            for p in politicas:
                print(f"{p.id:<5} {p.nombre:<20} {p.dias_aviso:<15} {p.porcentaje_reembolso}%")
            print("="*80)
            print("\nNOTA: Las políticas son de solo lectura y se configuran en la base de datos.")
    except Exception as e:
        print(f"ERROR: Error al cargar políticas: {e}")
    pausar()
