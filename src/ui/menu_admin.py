"""Menú de Administrador - Interfaz de Usuario por Consola

Interfaz para funciones administrativas del sistema.
Solo accesible para usuarios con rol 'administrador'.
"""
from datetime import datetime

from src.dao import ActividadDAO, DestinoDAO, PaqueteDAO, ReservaDAO
from src.dto import ActividadDTO, DestinoDTO, PaqueteDTO, UsuarioDTO
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
    destino_dao = DestinoDAO()
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
            dest = input("Ingrese nombre de destino a buscar (o Enter para todos): ")
            if dest:
                print(f"Mostrando destinos que coinciden con '{dest}'...")
                destinos = destino_dao.buscar_por_nombre(dest)
                mostrar_tabla_destinos(destinos)
            else:
                print("Mostrando todos los destinos...")
                destinos = destino_dao.listar_todos()
                mostrar_tabla_destinos(destinos)
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR DESTINO ===")
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
            try:
                nombre = validar_cancelacion(input("Nombre del destino: "))
                descripcion = validar_cancelacion(input("Descripción: "))
                costo_base_str = validar_cancelacion(input("Costo base del destino: "))
                costo_base = float(costo_base_str)
                
                print(f"Agregando destino '{nombre}'...")
                new_destino = DestinoDTO(None, nombre, descripcion, costo_base)
                new_destino.id = destino_dao.crear(new_destino)
                print(f"EXITO: Destino '{nombre}' agregado con ID: {new_destino.id}")
            except OperacionCancelada:
                print("\nINFO: Operación cancelada.")
            except Exception as e:
                print(f"ERROR: Error al agregar destino: {e}")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR DESTINO ===")
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
            try:
                destinos = destino_dao.listar_todos()
                print("Destinos disponibles:")
                for d in destinos:
                    print(f"- {d.nombre} (ID: {d.id})")
                    
                id_editar_str = validar_cancelacion(input("\nIngrese el ID del destino a editar: "))
                id_editar = int(id_editar_str)
                
                destino = destino_dao.obtener_por_id(id_editar) 
                if not destino:
                    print(f"ERROR: No se encontró destino con ID {id_editar}.")
                    pausar()
                    continue
                    
                print(f"\nDestino a editar: {destino.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (Enter para mantener '{destino.nombre}'): ") or destino.nombre
                nueva_descripcion = input("Nueva descripción (Enter para mantener): ") or destino.descripcion
                nuevo_costo_base = input(f"Nuevo costo base (Enter para mantener '{destino.costo_base}'): ") or destino.costo_base
                
                print(f"\nActualizando destino ID {id_editar}...")
                destino.nombre = nuevo_nombre
                destino.descripcion = nueva_descripcion
                destino.costo_base = float(nuevo_costo_base)
                actualizado = destino_dao.actualizar(id_editar, destino)
                
                if actualizado:
                    print(f"EXITO: Destino ID {id_editar} actualizado exitosamente.")
                else:
                    print(f"ERROR: No se pudo actualizar el destino ID {id_editar}.")
                    
            except OperacionCancelada:
                print("\nINFO: Operación cancelada.")
            except Exception as e:
                print(f"ERROR: Error al actualizar destino: {e}")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR DESTINO ===")
            destinos = destino_dao.listar_todos()
            print("Destinos disponibles:")
            for d in destinos:
                print(f"- {d.nombre} (ID: {d.id})")
            id_eliminar = int(input("\nIngrese el ID del destino a eliminar: "))
            destino = destino_dao.obtener_por_id(id_eliminar)
            if not destino:
                print(f"No se encontró destino con ID {id_eliminar}.")
                pausar()
                continue
            print(f"Destino a eliminar: {destino.nombre}")
            confirmar = input("¿Está seguro? (s/n): ")
            if confirmar.lower() != 's':    
                print("Eliminación cancelada.")
                pausar()
                continue
            print(f"Eliminando destino ID {id_eliminar}...")
            # Lógica para eliminar destino
            try:
                eliminado = destino_dao.eliminar(id_eliminar)
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
    """Submenú para gestión de actividades."""
    actividad_dao = ActividadDAO()
    destino_dao = DestinoDAO()
    
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
            actividades = actividad_dao.listar_todas()
            if not actividades:
                print("No hay actividades registradas.")
            else:
                mostrar_tabla_actividades(actividades)
            pausar()
        elif int(opcion) == 2:
            print("=== VIAJES AVENTURA: AGREGAR ACTIVIDAD ===")
            # Listar destinos disponibles
            destinos = destino_dao.listar_todos()
            if not destinos:
                print("No hay destinos disponibles. Cree destinos primero.")
                pausar()
                continue
            print("\nDestinos disponibles:")
            for d in destinos:
                print(f"  ID: {d.id} - {d.nombre}")
            
            try:
                nombre = input("\nNombre de la actividad: ")
                descripcion = input("Descripción: ")
                duracion = int(input("Duración (horas): "))
                precio = float(input("Precio base: "))
                destino_id = int(input("ID del destino: "))
                
                nueva_actividad = ActividadDTO(0, nombre, descripcion, duracion, precio, destino_id)
                id_creado = actividad_dao.crear(nueva_actividad)
                print(f"EXITO: Actividad creada con ID: {id_creado}")
            except Exception as e:
                print(f"ERROR: Error al crear actividad: {e}")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR ACTIVIDAD ===")
            try:
                id_editar = int(input("ID de la actividad a editar: "))
                actividad = actividad_dao.obtener_por_id(id_editar)
                if not actividad:
                    print(f"No se encontró actividad con ID {id_editar}")
                    pausar()
                    continue
                
                print(f"\nActividad actual: {actividad.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (Enter='{actividad.nombre}'): ") or actividad.nombre
                nueva_descripcion = input(f"Nueva descripción (Enter='{actividad.descripcion}'): ") or actividad.descripcion
                nueva_duracion = input(f"Nueva duración (Enter={actividad.duracion_horas}h): ")
                nuevo_precio = input(f"Nuevo precio (Enter=${actividad.precio_base}): ")
                nuevo_destino = input(f"Nuevo destino ID (Enter={actividad.destino_id}): ")
                
                actividad.nombre = nuevo_nombre
                actividad.descripcion = nueva_descripcion
                actividad.duracion_horas = int(nueva_duracion) if nueva_duracion else actividad.duracion_horas
                actividad.precio_base = float(nuevo_precio) if nuevo_precio else actividad.precio_base
                actividad.destino_id = int(nuevo_destino) if nuevo_destino else actividad.destino_id
                
                if actividad_dao.actualizar(id_editar, actividad):
                    print("EXITO: Actividad actualizada exitosamente")
                else:
                    print("ERROR: No se pudo actualizar la actividad")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR ACTIVIDAD ===")
            try:
                id_eliminar = int(input("ID de la actividad a eliminar: "))
                actividad = actividad_dao.obtener_por_id(id_eliminar)
                if not actividad:
                    print(f"No se encontró actividad con ID {id_eliminar}")
                    pausar()
                    continue
                
                print(f"\nActividad: {actividad.nombre}")
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == 's':
                    if actividad_dao.eliminar(id_eliminar):
                        print("EXITO: Actividad eliminada exitosamente")
                    else:
                        print("ERROR: No se pudo eliminar la actividad")
                else:
                    print("Eliminación cancelada")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_paquetes():
    """Submenú para gestión de paquetes."""
    paquete_dao = PaqueteDAO()
    
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
            paquetes = paquete_dao.listar_todos()
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
                politica_id = int(input("ID política de cancelación (ej: 1): "))
                
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
                
                nuevo_paquete = PaqueteDTO(0, nombre, fecha_inicio, fecha_fin, precio, cupos, politica_id)
                id_creado = paquete_dao.crear(nuevo_paquete)
                print(f"EXITO: Paquete creado con ID: {id_creado}")
            except Exception as e:
                print(f"ERROR: Error al crear paquete: {e}")
            pausar()
        elif int(opcion) == 3:
            print("=== VIAJES AVENTURA: EDITAR PAQUETE ===")
            try:
                id_editar = int(input("ID del paquete a editar: "))
                paquete = paquete_dao.obtener_por_id(id_editar)
                if not paquete:
                    print(f"No se encontró paquete con ID {id_editar}")
                    pausar()
                    continue
                
                print(f"\nPaquete actual: {paquete.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (Enter='{paquete.nombre}'): ") or paquete.nombre
                nuevo_precio = input(f"Nuevo precio (Enter=${paquete.precio_total}): ")
                nuevos_cupos = input(f"Nuevos cupos (Enter={paquete.cupos_disponibles}): ")
                
                paquete.nombre = nuevo_nombre
                paquete.precio_total = float(nuevo_precio) if nuevo_precio else paquete.precio_total
                paquete.cupos_disponibles = int(nuevos_cupos) if nuevos_cupos else paquete.cupos_disponibles
                
                if paquete_dao.actualizar(id_editar, paquete):
                    print("EXITO: Paquete actualizado exitosamente")
                else:
                    print("ERROR: No se pudo actualizar el paquete")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 4:
            print("=== VIAJES AVENTURA: ELIMINAR PAQUETE ===")
            try:
                id_eliminar = int(input("ID del paquete a eliminar: "))
                paquete = paquete_dao.obtener_por_id(id_eliminar)
                if not paquete:
                    print(f"No se encontró paquete con ID {id_eliminar}")
                    pausar()
                    continue
                
                print(f"\nPaquete: {paquete.nombre}")
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == 's':
                    if paquete_dao.eliminar(id_eliminar):
                        print("EXITO: Paquete eliminado exitosamente")
                    else:
                        print("ERROR: No se pudo eliminar el paquete")
                else:
                    print("Eliminación cancelada")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif int(opcion) == 5:
            break


def menu_admin_reportes():
    """Submenú para reportes administrativos."""
    from src.business.pago_manager import generar_reporte_ventas
    from src.dao.usuario_dao import UsuarioDAO
    from src.utils.constants import ESTADOS_RESERVA
    
    reserva_dao = ReservaDAO()
    usuario_dao = UsuarioDAO()
    
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
            print("\nFiltrar por estado:")
            print("0. Todas")
            for i, estado in enumerate(ESTADOS_RESERVA, 1):
                print(f"{i}. {estado}")
            filtro = input("\nSeleccione opción (Enter=Todas): ")
            
            try:
                if not filtro or filtro == '0':
                    # Listar todas - necesitaríamos un método listar_todas() en ReservaDAO
                    print("\nListando todas las reservas por estado:")
                    for estado in ESTADOS_RESERVA:
                        reservas = reserva_dao.listar_por_estado(estado)
                        if reservas:
                            print(f"\n--- {estado.upper()} ({len(reservas)}) ---")
                            mostrar_tabla_reservas(reservas)
                else:
                    estado_seleccionado = ESTADOS_RESERVA[int(filtro) - 1]
                    reservas = reserva_dao.listar_por_estado(estado_seleccionado)
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
                
                reporte = generar_reporte_ventas(fecha_inicio, fecha_fin)
                print("\n--- REPORTE DE VENTAS ---")
                print(f"Período: {reporte['fecha_inicio']} al {reporte['fecha_fin']}")
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
                clientes = usuario_dao.listar_por_rol('cliente')
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