"""Menú de Administrador - Interfaz de Usuario por Consola

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
    leer_opcion,
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
        print("4. Reservas")
        print("5. Usuarios")
        print("6. Políticas de Cancelación")
        print("7. Reportes")
        print("8. Cerrar Sesión")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 8):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        if opcion == 1:
            menu_admin_destinos()
        elif opcion == 2:
            menu_admin_actividades()
        elif opcion == 3:
            menu_admin_paquetes()
        elif opcion == 4:
            menu_admin_reservas()
        elif opcion == 5:
            menu_admin_usuarios()
        elif opcion == 6:
            menu_admin_politicas()
        elif opcion == 7:
            menu_admin_reportes()
        elif opcion == 8:
            break


def menu_admin_destinos():
    """Submenú para gestión de destinos."""
    destino_service = DestinoService()
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: DESTINOS ===")
        print("1. Listar Destinos")
        print("2. Agregar Destino")
        print("3. Editar Destino")
        print("4. Desactivar Destino")
        print("5. Reactivar Destino")
        print("6. Volver")
        opcion = leer_opcion()
        
        if not validar_opcion(opcion, 1, 6):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
            print("=== VIAJES AVENTURA: LISTAR DESTINOS ===")
            destinos = destino_service.listar_todos_destinos_admin()
            if not destinos:
                print("No hay destinos registrados.")
            else:
                # Mostrar tabla con estado
                print("="*110)
                print(f"{'ID':<5} {'NOMBRE':<25} {'COSTO BASE':<15} {'CUPOS':<10} {'POLÍTICA':<12} {'ESTADO':<10}")
                print("="*110)
                for d in destinos:
                    politica = "Flexible" if d['politica_id'] == 1 else "Estricta"
                    estado = "ACTIVO" if d['activo'] else "INACTIVO"
                    print(f"{d['id']:<5} {d['nombre'][:24]:<25} ${d['costo_base']:>12,} {d['cupos_disponibles']:<10} {politica:<12} {estado:<10}".replace(",", "."))
                print("="*110)
            pausar()
        elif opcion == 2:
            print("=== VIAJES AVENTURA: AGREGAR DESTINO ===")
            print("(Escriba 'cancelar' para abortar)\n")
            try:
                nombre = validar_cancelacion(input("Nombre del destino: "))
                descripcion = validar_cancelacion(input("Descripción: "))
                costo_base_str = validar_cancelacion(input("Costo base del destino: "))
                costo_base = float(costo_base_str.replace("$", "").replace(".", "").replace(",", ""))
                cupos_str = validar_cancelacion(input("Cupos disponibles (Enter=50): ")) or "50"
                cupos = int(cupos_str.strip())
                
                # Seleccionar política de cancelación
                print("\nPolíticas de cancelación disponibles:")
                print("  1. Flexible (3 días aviso, 100% reembolso)")
                print("  2. Estricta (7 días aviso, 50% reembolso)")
                politica_str = input("Seleccione política (1 o 2, Enter=1 Flexible): ") or "1"
                while politica_str not in ["1", "2"]:
                    print("ERROR: Opción inválida. Debe ser 1 (Flexible) o 2 (Estricta).")
                    politica_str = input("Seleccione política (1 o 2): ")
                politica_id = int(politica_str)
                
                print(f"Agregando destino '{nombre}'...")
                new_destino = destino_service.crear_destino(nombre, "País", descripcion, costo_base, cupos, politica_id)
                print(f"EXITO: Destino '{nombre}' agregado con ID: {new_destino.id}")
            except OperacionCancelada:
                print("\nINFO: Operación cancelada.")
            except Exception as e:
                print(f"ERROR: Error al agregar destino: {e}")
            pausar()
        elif opcion == 3:
            print("=== VIAJES AVENTURA: EDITAR DESTINO ===")
            print("(Escriba 'cancelar' para abortar)\n")
            try:
                destinos = destino_service.listar_todos_destinos()
                if destinos:
                    print("Destinos disponibles:")
                    mostrar_tabla_destinos(destinos)
                else:
                    print("No hay destinos registrados.")
                    pausar()
                    continue
                id_editar_str = validar_cancelacion(input("\nIngrese el ID del destino a editar: "))
                id_editar = int(id_editar_str)
                
                destino = destino_service.obtener_destino(id_editar)
                if not destino:
                    print(f"ERROR: No se encontró destino con ID {id_editar}.")
                    pausar()
                    continue
                
                # Mostrar política actual
                politica_actual = "Flexible" if destino.politica_id == 1 else "Estricta"
                    
                print(f"\nDestino a editar: {destino.nombre}")
                print(f"Política actual: {politica_actual}")
                nuevo_nombre = input(f"Nuevo nombre (Enter para mantener '{destino.nombre}'): ") or destino.nombre
                nueva_descripcion = input("Nueva descripción (Enter para mantener): ") or destino.descripcion
                nuevo_costo_base_str = input(f"Nuevo costo base (Enter para mantener '{destino.costo_base}'): ").replace("$", "").replace(".", "").replace(",", "")
                nuevo_costo_base = float(nuevo_costo_base_str) if nuevo_costo_base_str else destino.costo_base
                nuevos_cupos_str = input(f"Nuevos cupos (Enter para mantener '{destino.cupos_disponibles}'): ")
                nuevos_cupos = int(nuevos_cupos_str) if nuevos_cupos_str else destino.cupos_disponibles
                
                # Opción de cambiar política
                print("\nPolíticas de cancelación:")
                print("  1. Flexible (3 días aviso, 100% reembolso)")
                print("  2. Estricta (7 días aviso, 50% reembolso)")
                nueva_politica_str = input(f"Nueva política (1 o 2, Enter para mantener '{politica_actual}'): ")
                if nueva_politica_str == "":
                    nueva_politica_id = destino.politica_id
                elif nueva_politica_str in ["1", "2"]:
                    nueva_politica_id = int(nueva_politica_str)
                else:
                    print("ERROR: Política inválida. Debe ser 1 (Flexible) o 2 (Estricta).")
                    pausar()
                    continue
                
                print(f"\nActualizando destino ID {id_editar}...")
                destino_actualizado = destino_service.actualizar_destino(
                    id_editar,
                    nuevo_nombre,
                    "País",
                    nueva_descripcion,
                    nuevo_costo_base,
                    nuevos_cupos,
                    nueva_politica_id
                )
                print(f"EXITO: Destino '{destino_actualizado.nombre}' actualizado correctamente.")
            except OperacionCancelada:
                print("\nINFO: Operación cancelada.")
            except Exception as e:
                print(f"ERROR: Error al editar destino: {e}")
            pausar()
        elif opcion == 4:
            print("=== VIAJES AVENTURA: DESACTIVAR DESTINO ===")
            destinos = destino_service.listar_todos_destinos_admin()
            activos = [d for d in destinos if d['activo']]
            if activos:
                print("Destinos activos:")
                print("="*80)
                print(f"{'ID':<5} {'NOMBRE':<30} {'CUPOS':<10}")
                print("="*80)
                for d in activos:
                    print(f"{d['id']:<5} {d['nombre'][:29]:<30} {d['cupos_disponibles']:<10}")
                print("="*80)
            else:
                print("No hay destinos activos.")
                pausar()
                continue
            try:
                id_desactivar = int(input("\nIngrese el ID del destino a desactivar: "))
                destino = destino_service.obtener_destino(id_desactivar)
                if not destino:
                    print(f"No se encontró destino activo con ID {id_desactivar}.")
                    pausar()
                    continue
                print(f"Destino a desactivar: {destino.nombre}")
                confirmar = input("¿Está seguro? (s/n): ")
                if confirmar.lower() != 's':    
                    print("Operación cancelada.")
                    pausar()
                    continue
                desactivado = destino_service.eliminar_destino(id_desactivar)
                if desactivado:
                    print(f"EXITO: Destino '{destino.nombre}' desactivado exitosamente.")
                else:
                    print(f"No se pudo desactivar el destino ID {id_desactivar}.")
            except ValueError:
                print("ERROR: Debe ingresar un número válido.")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
        elif opcion == 5:
            print("=== VIAJES AVENTURA: REACTIVAR DESTINO ===")
            destinos = destino_service.listar_todos_destinos_admin()
            inactivos = [d for d in destinos if not d['activo']]
            if inactivos:
                print("Destinos inactivos:")
                print("="*80)
                print(f"{'ID':<5} {'NOMBRE':<30} {'CUPOS':<10}")
                print("="*80)
                for d in inactivos:
                    print(f"{d['id']:<5} {d['nombre'][:29]:<30} {d['cupos_disponibles']:<10}")
                print("="*80)
            else:
                print("No hay destinos inactivos para reactivar.")
                pausar()
                continue
            try:
                id_reactivar = int(input("\nIngrese el ID del destino a reactivar: "))
                # Verificar que está en la lista de inactivos
                destino_inactivo = next((d for d in inactivos if d['id'] == id_reactivar), None)
                if not destino_inactivo:
                    print(f"No se encontró destino inactivo con ID {id_reactivar}.")
                    pausar()
                    continue
                reactivado = destino_service.reactivar_destino(id_reactivar)
                if reactivado:
                    print(f"EXITO: Destino '{destino_inactivo['nombre']}' reactivado exitosamente.")
                else:
                    print(f"No se pudo reactivar el destino ID {id_reactivar}.")
            except ValueError:
                print("ERROR: Debe ingresar un número válido.")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
        elif opcion == 6:
            break


def menu_admin_actividades():
    """Submenú para gestión de actividades."""
    actividad_service = ActividadService()
    destino_service = DestinoService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: ACTIVIDADES ===")
        print("1. Listar Actividades")
        print("2. Agregar Actividad")
        print("3. Editar Actividad")
        print("4. Desactivar Actividad")
        print("5. Reactivar Actividad")
        print("6. Volver")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 6):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
            print("=== VIAJES AVENTURA: LISTAR ACTIVIDADES ===")
            actividades = actividad_service.listar_todas_actividades_admin()
            if not actividades:
                print("No hay actividades registradas.")
            else:
                print("="*100)
                print(f"{'ID':<5} {'NOMBRE':<25} {'DESTINO':<20} {'PRECIO':<12} {'ESTADO':<10}")
                print("="*100)
                for a in actividades:
                    destino = destino_service.obtener_destino(a['destino_id'])
                    destino_nombre = destino.nombre[:19] if destino else "Desconocido"
                    estado = "ACTIVO" if a['activo'] else "INACTIVO"
                    print(f"{a['id']:<5} {a['nombre'][:24]:<25} {destino_nombre:<20} ${a['precio_base']:>10,} {estado:<10}".replace(",", "."))
                print("="*100)
            pausar()
        elif opcion == 2:
            print("=== VIAJES AVENTURA: AGREGAR ACTIVIDAD ===")
            print("(Escriba 'cancelar' para abortar)\n")
            # Listar destinos disponibles PRIMERO
            destinos = destino_service.listar_todos_destinos()
            if not destinos:
                print("No hay destinos disponibles. Cree destinos primero.")
                pausar()
                continue
            print("Destinos disponibles:")
            mostrar_tabla_destinos(destinos)
            
            try:
                # Elegir destino PRIMERO
                destino_id_str = input("\nID del destino para la actividad (o 'cancelar'): ")
                if destino_id_str.lower() == 'cancelar':
                    print("\nINFO: Operación cancelada.")
                    pausar()
                    continue
                destino_id = int(destino_id_str)
                if not destino_service.obtener_destino(destino_id):
                    print(f"ERROR: No existe destino con ID {destino_id}")
                    pausar()
                    continue
                
                nombre = input("Nombre de la actividad: ")
                if not nombre:
                    print("ERROR: El nombre no puede estar vacío.")
                    pausar()
                    continue
                    
                descripcion = input("Descripción: ")
                
                duracion_str = input("Duración (horas): ")
                if not duracion_str:
                    print("ERROR: La duración no puede estar vacía.")
                    pausar()
                    continue
                duracion = int(duracion_str)
                
                precio_str = input("Precio base: ")
                if not precio_str:
                    print("ERROR: El precio no puede estar vacío.")
                    pausar()
                    continue
                precio = int(precio_str)
                
                nueva_actividad = actividad_service.crear_actividad(nombre, descripcion, duracion, precio, destino_id)
                print(f"EXITO: Actividad creada con ID: {nueva_actividad.id}")
            except ValueError:
                print("ERROR: Debe ingresar valores numéricos válidos.")
            except Exception as e:
                print(f"ERROR: Error al crear actividad: {e}")
            pausar()
        elif opcion == 3:
            print("=== VIAJES AVENTURA: EDITAR ACTIVIDAD ===")
            try:
                actividades = actividad_service.listar_todas_actividades()
                if not actividades:
                    print("No hay actividades registradas.")
                else:
                    mostrar_tabla_actividades(actividades)
                id_editar = int(input("\nID de la actividad a editar: "))
                actividad = actividad_service.obtener_actividad(id_editar)
                if not actividad:
                    print(f"No se encontró actividad con ID {id_editar}")
                    pausar()
                    continue
                
                print(f"\nActividad actual: {actividad.nombre}")
                print(f"Destino actual ID: {actividad.destino_id}")
                
                nuevo_nombre = input(f"Nuevo nombre (Enter='{actividad.nombre}'): ") or actividad.nombre
                nueva_descripcion = input(f"Nueva descripción (Enter='{actividad.descripcion}'): ") or actividad.descripcion
                nueva_duracion = input(f"Nueva duración (Enter={actividad.duracion_horas}h): ")
                nuevo_precio = input(f"Nuevo precio (Enter=${actividad.precio_base}): ")
                
                # Mostrar destinos disponibles para cambiar
                print("\nDestinos disponibles:")
                destinos = destino_service.listar_todos_destinos()
                for d in destinos:
                    print(f"  ID {d.id}: {d.nombre}")
                nuevo_destino_str = input(f"Nuevo destino ID (Enter para mantener {actividad.destino_id}): ")
                
                # Validar destino si se cambió
                nuevo_destino_id = actividad.destino_id
                if nuevo_destino_str:
                    nuevo_destino_id = int(nuevo_destino_str)
                    if not destino_service.obtener_destino(nuevo_destino_id):
                        print(f"ERROR: No existe destino con ID {nuevo_destino_id}")
                        pausar()
                        continue
                
                actividad.nombre = nuevo_nombre
                actividad.descripcion = nueva_descripcion
                actividad.duracion_horas = int(nueva_duracion) if nueva_duracion else actividad.duracion_horas
                actividad.precio_base = int(nuevo_precio) if nuevo_precio else actividad.precio_base
                actividad.destino_id = nuevo_destino_id
                
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
        elif opcion == 4:
            print("=== VIAJES AVENTURA: DESACTIVAR ACTIVIDAD ===")
            try:
                actividades = actividad_service.listar_todas_actividades_admin()
                activas = [a for a in actividades if a['activo']]
                if not activas:
                    print("No hay actividades activas.")
                    pausar()
                    continue
                print("="*80)
                print(f"{'ID':<5} {'NOMBRE':<30} {'PRECIO':<15}")
                print("="*80)
                for a in activas:
                    print(f"{a['id']:<5} {a['nombre'][:29]:<30} ${a['precio_base']:>12,}".replace(",", "."))
                print("="*80)
                
                id_desactivar = int(input("\nID de la actividad a desactivar: "))
                actividad = actividad_service.obtener_actividad(id_desactivar)
                if not actividad:
                    print(f"No se encontró actividad activa con ID {id_desactivar}")
                    pausar()
                    continue
                
                print(f"\nActividad: {actividad.nombre}")
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == 's':
                    if actividad_service.eliminar_actividad(id_desactivar):
                        print("EXITO: Actividad desactivada exitosamente")
                    else:
                        print("ERROR: No se pudo desactivar la actividad")
                else:
                    print("Operación cancelada")
            except ValueError:
                print("ERROR: Debe ingresar un número válido.")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
        elif opcion == 5:
            print("=== VIAJES AVENTURA: REACTIVAR ACTIVIDAD ===")
            try:
                actividades = actividad_service.listar_todas_actividades_admin()
                inactivas = [a for a in actividades if not a['activo']]
                if not inactivas:
                    print("No hay actividades inactivas para reactivar.")
                    pausar()
                    continue
                print("="*80)
                print(f"{'ID':<5} {'NOMBRE':<30} {'PRECIO':<15}")
                print("="*80)
                for a in inactivas:
                    print(f"{a['id']:<5} {a['nombre'][:29]:<30} ${a['precio_base']:>12,}".replace(",", "."))
                print("="*80)
                
                id_reactivar = int(input("\nID de la actividad a reactivar: "))
                actividad_inactiva = next((a for a in inactivas if a['id'] == id_reactivar), None)
                if not actividad_inactiva:
                    print(f"No se encontró actividad inactiva con ID {id_reactivar}")
                    pausar()
                    continue
                
                if actividad_service.reactivar_actividad(id_reactivar):
                    print(f"EXITO: Actividad '{actividad_inactiva['nombre']}' reactivada exitosamente")
                else:
                    print("ERROR: No se pudo reactivar la actividad")
            except ValueError:
                print("ERROR: Debe ingresar un número válido.")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
        elif opcion == 6:
            break


def menu_admin_paquetes():
    """Submenú para gestión de paquetes."""
    destino_service = DestinoService()
    paquete_service = PaqueteService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: PAQUETES ===")
        print("1. Listar Paquetes")
        print("2. Agregar Paquete")
        print("3. Editar Paquete")
        print("4. Gestionar Actividades del Paquete")
        print("5. Desactivar Paquete")
        print("6. Reactivar Paquete")
        print("7. Volver")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 7):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
            print("=== VIAJES AVENTURA: LISTAR PAQUETES ===")
            paquetes = paquete_service.listar_todos_paquetes()
            if not paquetes:
                print("No hay paquetes registrados.")
            else:
                mostrar_tabla_paquetes(paquetes)
            pausar()
        elif opcion == 2:
            print("=== VIAJES AVENTURA: AGREGAR PAQUETE ===")
            try:
                destinos = destino_service.listar_todos_destinos()
                if not destinos:
                    print("No hay destinos registrados. Cree destinos primero.")
                    pausar()
                    continue
                print("\nDestinos disponibles:")
                mostrar_tabla_destinos(destinos)
                while True:
                    destino_id = int(input("\nID del destino para el paquete: "))
                    if not destino_service.obtener_destino(destino_id):
                        print(f"No existe un destino con ID {destino_id}. Intente nuevamente.")
                        pausar()
                        continue
                    else:
                        break
                nombre = input("\nNombre del paquete: ")
                descripcion = input("Descripción del paquete: ")
                
                # Validar fechas con retry
                while True:
                    fecha_inicio_str = input("Fecha inicio (YYYY-MM-DD): ")
                    if not fecha_inicio_str:
                        print("ERROR: La fecha de inicio es obligatoria.")
                        continue
                    try:
                        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("ERROR: Formato inválido. Use YYYY-MM-DD (ej: 2025-01-15)")
                
                while True:
                    fecha_fin_str = input("Fecha fin (YYYY-MM-DD): ")
                    if not fecha_fin_str:
                        print("ERROR: La fecha de fin es obligatoria.")
                        continue
                    try:
                        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
                        if fecha_fin <= fecha_inicio:
                            print("ERROR: La fecha de fin debe ser posterior a la de inicio.")
                            continue
                        break
                    except ValueError:
                        print("ERROR: Formato inválido. Use YYYY-MM-DD (ej: 2025-01-15)")
                
                precio = int(input("Precio total: "))
                cupos = int(input("Cupos disponibles: "))
                
                # Mostrar políticas disponibles con nombres
                print("\nPolíticas de cancelación:")
                print("  1. Flexible (3 días aviso, 100% reembolso)")
                print("  2. Estricta (7 días aviso, 50% reembolso)")
                politica_str = input("Seleccione política (1 o 2): ")
                while politica_str not in ["1", "2"]:
                    print("ERROR: Opción inválida. Debe ser 1 (Flexible) o 2 (Estricta).")
                    politica_str = input("Seleccione política (1 o 2): ")
                politica_id = int(politica_str)
                
                nuevo_paquete = paquete_service.crear_paquete(
                    nombre=nombre,
                    descripcion=descripcion,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    precio_total=precio,
                    cupos_disponibles=cupos,
                    politica_id=politica_id,
                    destino_id=destino_id
                )
                print(f"EXITO: Paquete creado con ID: {nuevo_paquete.id}")
            except Exception as e:
                print(f"ERROR: Error al crear paquete: {e}")
            pausar()
        elif opcion == 3:
            print("=== VIAJES AVENTURA: EDITAR PAQUETE ===")
            try:
                paquetes = paquete_service.listar_todos_paquetes()
                if not paquetes:
                    print("No hay paquetes registrados.")
                else:
                    mostrar_tabla_paquetes(paquetes)
                id_editar = int(input("\nID del paquete a editar: "))
                paquete = paquete_service.obtener_paquete(id_editar)
                if not paquete:
                    print(f"No se encontró paquete con ID {id_editar}")
                    pausar()
                    continue
                
                print(f"\nPaquete actual: {paquete.nombre}")
                print(f"Fecha inicio actual: {paquete.fecha_inicio}")
                print(f"Fecha fin actual: {paquete.fecha_fin}")
                politica_actual = "Flexible" if paquete.politica_id == 1 else "Estricta"
                print(f"Política actual: {politica_actual}")
                
                nuevo_nombre = input(f"Nuevo nombre (Enter='{paquete.nombre}'): ") or paquete.nombre
                nueva_descripcion = input("Nueva descripción (Enter para mantener): ") or paquete.descripcion
                nuevo_precio = input(f"Nuevo precio (Enter=${paquete.precio_total}): ")
                nuevos_cupos = input(f"Nuevos cupos (Enter={paquete.cupos_disponibles}): ")
                
                # Fechas
                nueva_fecha_inicio_str = input("Nueva fecha inicio YYYY-MM-DD (Enter para mantener): ")
                nueva_fecha_fin_str = input("Nueva fecha fin YYYY-MM-DD (Enter para mantener): ")
                
                # Opción de cambiar política
                print("\nPolíticas de cancelación:")
                print("  1. Flexible (3 días aviso, 100% reembolso)")
                print("  2. Estricta (7 días aviso, 50% reembolso)")
                nueva_politica_str = input(f"Nueva política (1 o 2, Enter para mantener '{politica_actual}'): ")
                if nueva_politica_str == "":
                    nueva_politica_id = paquete.politica_id
                elif nueva_politica_str in ["1", "2"]:
                    nueva_politica_id = int(nueva_politica_str)
                else:
                    print("ERROR: Política inválida. Debe ser 1 (Flexible) o 2 (Estricta).")
                    pausar()
                    continue
                
                paquete.nombre = nuevo_nombre
                paquete.descripcion = nueva_descripcion
                paquete.precio_total = int(nuevo_precio) if nuevo_precio else paquete.precio_total
                paquete.cupos_disponibles = int(nuevos_cupos) if nuevos_cupos else paquete.cupos_disponibles
                paquete.politica_id = nueva_politica_id
                
                # Parsear fechas si se proporcionaron
                if nueva_fecha_inicio_str:
                    paquete.fecha_inicio = datetime.strptime(nueva_fecha_inicio_str, "%Y-%m-%d")
                if nueva_fecha_fin_str:
                    paquete.fecha_fin = datetime.strptime(nueva_fecha_fin_str, "%Y-%m-%d")
                
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
        elif opcion == 4:
            # Gestionar actividades del paquete
            print("=== VIAJES AVENTURA: GESTIONAR ACTIVIDADES DEL PAQUETE ===")
            try:
                from src.dao.paquete_actividad_dao import PaqueteActividadDAO
                paquete_actividad_dao = PaqueteActividadDAO()
                actividad_service = ActividadService()
                
                paquetes = paquete_service.listar_todos_paquetes()
                if not paquetes:
                    print("No hay paquetes registrados.")
                    pausar()
                    continue
                
                mostrar_tabla_paquetes(paquetes)
                paquete_id = int(input("\nID del paquete a gestionar: "))
                paquete = paquete_service.obtener_paquete(paquete_id)
                if not paquete:
                    print(f"No se encontró paquete con ID {paquete_id}")
                    pausar()
                    continue
                
                while True:
                    limpiar_pantalla()
                    print(f"=== ACTIVIDADES DEL PAQUETE: {paquete.nombre} ===\n")
                    
                    # Mostrar actividades actuales
                    actividades_paquete = paquete_actividad_dao.listar_actividades_por_paquete(paquete_id)
                    if actividades_paquete:
                        print("Actividades incluidas:")
                        print("-"*60)
                        for a in actividades_paquete:
                            print(f"  ID {a['id']}: {a['nombre']} (${a['precio_base']:,})".replace(",", "."))
                        print("-"*60)
                    else:
                        print("Este paquete no tiene actividades asociadas.\n")
                    
                    print("\n1. Agregar actividad")
                    print("2. Quitar actividad")
                    print("3. Volver")
                    sub_opcion = leer_opcion()
                    
                    if sub_opcion == 1:
                        # Mostrar actividades disponibles
                        todas_actividades = actividad_service.listar_todas_actividades()
                        ids_actuales = [a['id'] for a in actividades_paquete]
                        disponibles = [a for a in todas_actividades if a.id not in ids_actuales]
                        
                        if not disponibles:
                            print("\nNo hay más actividades disponibles para agregar.")
                            pausar()
                            continue
                        
                        print("\nActividades disponibles:")
                        for a in disponibles:
                            print(f"  ID {a.id}: {a.nombre} (${a.precio_base:,})".replace(",", "."))
                        
                        actividad_id = int(input("\nID de la actividad a agregar: "))
                        if paquete_actividad_dao.agregar_actividad(paquete_id, actividad_id):
                            print("EXITO: Actividad agregada al paquete.")
                        else:
                            print("ERROR: No se pudo agregar la actividad.")
                        pausar()
                    elif sub_opcion == 2:
                        if not actividades_paquete:
                            print("\nNo hay actividades para quitar.")
                            pausar()
                            continue
                        
                        actividad_id = int(input("\nID de la actividad a quitar: "))
                        if paquete_actividad_dao.eliminar_actividad(paquete_id, actividad_id):
                            print("EXITO: Actividad quitada del paquete.")
                        else:
                            print("ERROR: No se pudo quitar la actividad.")
                        pausar()
                    elif sub_opcion == 3:
                        break
            except ValueError:
                print("ERROR: Debe ingresar un número válido.")
                pausar()
            except Exception as e:
                print(f"ERROR: {e}")
                pausar()
        elif opcion == 5:
            print("=== VIAJES AVENTURA: DESACTIVAR PAQUETE ===")
            try:
                paquetes = paquete_service.listar_todos_paquetes_admin()
                activos = [p for p in paquetes if p['activo']]
                if not activos:
                    print("No hay paquetes activos.")
                    pausar()
                    continue
                print("Paquetes activos:")
                print("="*90)
                print(f"{'ID':<5} {'NOMBRE':<30} {'PRECIO':<15} {'CUPOS':<10} {'ESTADO':<10}")
                print("="*90)
                for p in activos:
                    print(f"{p['id']:<5} {p['nombre'][:29]:<30} ${p['precio_total']:>12,} {p['cupos_disponibles']:<10} ACTIVO".replace(",", "."))
                print("="*90)
                
                id_desactivar = int(input("\nID del paquete a desactivar: "))
                paquete = paquete_service.obtener_paquete(id_desactivar)
                if not paquete:
                    print(f"No se encontró paquete activo con ID {id_desactivar}")
                    pausar()
                    continue
                
                print(f"\nPaquete: {paquete.nombre}")
                confirmacion = input("¿Está seguro? (s/n): ")
                if confirmacion.lower() == 's':
                    if paquete_service.eliminar_paquete(id_desactivar):
                        print("EXITO: Paquete desactivado exitosamente")
                    else:
                        print("ERROR: No se pudo desactivar el paquete")
                else:
                    print("Operación cancelada")
            except ValueError:
                print("ERROR: Debe ingresar un número válido.")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
        elif opcion == 6:
            print("=== VIAJES AVENTURA: REACTIVAR PAQUETE ===")
            try:
                paquetes = paquete_service.listar_todos_paquetes_admin()
                inactivos = [p for p in paquetes if not p['activo']]
                if not inactivos:
                    print("No hay paquetes inactivos para reactivar.")
                    pausar()
                    continue
                print("Paquetes inactivos:")
                print("="*90)
                print(f"{'ID':<5} {'NOMBRE':<30} {'PRECIO':<15} {'CUPOS':<10}")
                print("="*90)
                for p in inactivos:
                    print(f"{p['id']:<5} {p['nombre'][:29]:<30} ${p['precio_total']:>12,} {p['cupos_disponibles']:<10}".replace(",", "."))
                print("="*90)
                
                id_reactivar = int(input("\nID del paquete a reactivar: "))
                paquete_inactivo = next((p for p in inactivos if p['id'] == id_reactivar), None)
                if not paquete_inactivo:
                    print(f"No se encontró paquete inactivo con ID {id_reactivar}")
                    pausar()
                    continue
                
                if paquete_service.reactivar_paquete(id_reactivar):
                    print(f"EXITO: Paquete '{paquete_inactivo['nombre']}' reactivado exitosamente")
                else:
                    print("ERROR: No se pudo reactivar el paquete")
            except ValueError:
                print("ERROR: Debe ingresar un número válido.")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
        elif opcion == 7:
            break


def menu_admin_usuarios():
    """Submenú para gestión de usuarios."""
    usuario_service = UsuarioService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: GESTIÓN DE USUARIOS ===")
        print("1. Ver todos los Usuarios")
        print("2. Ver solo Clientes")
        print("3. Ver solo Administradores")
        print("4. Buscar Usuario por Email")
        print("5. Volver")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
            # Ver todos los usuarios
            limpiar_pantalla()
            print("=== TODOS LOS USUARIOS ===\n")
            try:
                usuarios = usuario_service.listar_todos_usuarios()
                mostrar_tabla_usuarios(usuarios)
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 2:
            # Ver solo clientes
            limpiar_pantalla()
            print("=== USUARIOS CLIENTES ===\n")
            try:
                usuarios = usuario_service.listar_todos_usuarios()
                clientes = [u for u in usuarios if u.rol == "CLIENTE"]
                mostrar_tabla_usuarios(clientes)
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 3:
            # Ver solo administradores
            limpiar_pantalla()
            print("=== USUARIOS ADMINISTRADORES ===\n")
            try:
                usuarios = usuario_service.listar_todos_usuarios()
                admins = [u for u in usuarios if u.rol == "ADMIN"]
                mostrar_tabla_usuarios(admins)
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 4:
            # Buscar por email
            limpiar_pantalla()
            print("=== BUSCAR USUARIO ===\n")
            try:
                email = input("Ingrese email a buscar: ")
                usuario = usuario_service.obtener_usuario_por_email(email)
                if usuario:
                    print("\n--- Usuario encontrado ---")
                    print(f"ID: {usuario.id}")
                    print(f"Nombre: {usuario.nombre}")
                    print(f"Email: {usuario.email}")
                    print(f"Rol: {usuario.rol}")
                    print(f"Fecha registro: {usuario.fecha_registro}")
                    
                    # Mostrar reservas del usuario
                    print("\n--- Reservas del usuario ---")
                    reserva_service = ReservaService()
                    reservas = reserva_service.listar_reservas_cliente(usuario.id)
                    if reservas:
                        mostrar_tabla_reservas(reservas)
                    else:
                        print("Este usuario no tiene reservas.")
                else:
                    print(f"No se encontró usuario con email '{email}'")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 5:
            break


def mostrar_tabla_usuarios(usuarios: list) -> None:
    """Muestra lista de usuarios en formato tabla."""
    if not usuarios:
        print("No hay usuarios para mostrar.")
        return
    
    print("="*100)
    print(f"{'ID':<5} {'NOMBRE':<25} {'EMAIL':<35} {'ROL':<10} {'FECHA REGISTRO':<20}")
    print("="*100)
    
    for u in usuarios:
        fecha = str(u.fecha_registro)[:10] if u.fecha_registro else "N/A"
        nombre = (u.nombre[:22] + "...") if len(u.nombre) > 25 else u.nombre
        email = (u.email[:32] + "...") if len(u.email) > 35 else u.email
        print(f"{u.id:<5} {nombre:<25} {email:<35} {u.rol:<10} {fecha:<20}")
    
    print("="*100)
    print(f"\nTotal: {len(usuarios)} usuario(s)\n")


def menu_admin_reservas():
    """Submenú para gestión de reservas por el administrador."""
    from src.utils.constants import ESTADOS_RESERVA
    
    reserva_service = ReservaService()
    usuario_service = UsuarioService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: GESTIÓN DE RESERVAS ===")
        print("1. Ver Reservas Pagadas (pendientes de confirmar)")
        print("2. Confirmar Reserva Pagada")
        print("3. Cancelar Reserva")
        print("4. Ver todas las Reservas")
        print("5. Volver")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
            # Ver reservas pagadas (pendientes de confirmar por admin)
            limpiar_pantalla()
            print("=== RESERVAS PAGADAS (PENDIENTES DE CONFIRMAR) ===\n")
            try:
                todas_reservas = reserva_service.listar_todas_reservas()
                pagadas = [r for r in todas_reservas if r.estado == "PAGADA"]
                
                if not pagadas:
                    print("No hay reservas pagadas pendientes de confirmar.")
                else:
                    print(f"Total de reservas pagadas por confirmar: {len(pagadas)}\n")
                    mostrar_tabla_reservas(pagadas)
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 2:
            # Confirmar reserva pagada
            limpiar_pantalla()
            print("=== CONFIRMAR RESERVA PAGADA ===\n")
            try:
                # Mostrar solo las pagadas
                todas_reservas = reserva_service.listar_todas_reservas()
                pagadas = [r for r in todas_reservas if r.estado == "PAGADA"]
                
                if not pagadas:
                    print("No hay reservas pagadas para confirmar.")
                    pausar()
                    continue
                
                print("Reservas pagadas (pendientes de confirmación):")
                mostrar_tabla_reservas(pagadas)
                
                reserva_id = int(input("\nID de la reserva a confirmar (0 para cancelar): "))
                if reserva_id == 0:
                    continue
                
                reserva = reserva_service.obtener_reserva(reserva_id)
                if not reserva:
                    print("ERROR: Reserva no encontrada")
                    pausar()
                    continue
                
                if reserva.estado != "PAGADA":
                    print(f"ERROR: La reserva está en estado '{reserva.estado}'")
                    print("Solo se pueden confirmar reservas que ya estén PAGADAS")
                    pausar()
                    continue
                
                # Mostrar información del cliente
                cliente = usuario_service.obtener_usuario(reserva.usuario_id)
                cliente_nombre = cliente.nombre if cliente else "Desconocido"
                
                print("\n--- Detalles de la reserva ---")
                print(f"Cliente: {cliente_nombre}")
                print(f"Monto: ${int(reserva.monto_total):,}".replace(",", "."))
                print(f"Personas: {reserva.numero_personas}")
                
                confirmacion = input("\n¿Confirmar esta reserva? (s/n): ")
                if confirmacion.lower() == 's':
                    if reserva_service.confirmar_reserva(reserva_id):
                        print("EXITO: Reserva confirmada exitosamente")
                    else:
                        print("ERROR: No se pudo confirmar la reserva")
                else:
                    print("Operación cancelada")
            except ValueError:
                print("ERROR: ID inválido")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 3:
            # Cancelar reserva (admin)
            limpiar_pantalla()
            print("=== CANCELAR RESERVA (ADMIN) ===\n")
            try:
                # Mostrar reservas que se pueden cancelar
                todas_reservas = reserva_service.listar_todas_reservas()
                cancelables = [r for r in todas_reservas if r.estado in ["PENDIENTE", "CONFIRMADA"]]
                
                if not cancelables:
                    print("No hay reservas que se puedan cancelar.")
                    pausar()
                    continue
                
                print("Reservas que se pueden cancelar:")
                mostrar_tabla_reservas(cancelables)
                
                reserva_id = int(input("\nID de la reserva a cancelar (0 para volver): "))
                if reserva_id == 0:
                    continue
                
                reserva = reserva_service.obtener_reserva(reserva_id)
                if not reserva:
                    print("ERROR: Reserva no encontrada")
                    pausar()
                    continue
                
                if reserva.estado not in ["PENDIENTE", "CONFIRMADA"]:
                    print(f"ERROR: No se puede cancelar una reserva en estado '{reserva.estado}'")
                    pausar()
                    continue
                
                cliente = usuario_service.obtener_usuario(reserva.usuario_id)
                cliente_nombre = cliente.nombre if cliente else "Desconocido"
                
                print("\n--- Detalles de la reserva ---")
                print(f"Cliente: {cliente_nombre}")
                print(f"Estado actual: {reserva.estado}")
                print(f"Monto: ${int(reserva.monto_total):,}".replace(",", "."))
                
                confirmacion = input("\n¿Cancelar esta reserva? (s/n): ")
                if confirmacion.lower() == 's':
                    # Usar cancelar sin validación de política para admin
                    from src.dao.reserva_dao import ReservaDAO
                    reserva_dao = ReservaDAO()
                    if reserva_dao.cancelar(reserva_id):
                        print("EXITO: Reserva cancelada por administrador")
                        print("Los cupos han sido devueltos")
                    else:
                        print("ERROR: No se pudo cancelar la reserva")
                else:
                    print("Operación cancelada")
            except ValueError:
                print("ERROR: ID inválido")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 4:
            # Ver todas las reservas
            limpiar_pantalla()
            print("=== TODAS LAS RESERVAS ===\n")
            print("Filtrar por estado:")
            print("0. Todas")
            for i, estado in enumerate(ESTADOS_RESERVA, 1):
                print(f"{i}. {estado}")
            filtro = input("\nSeleccione opción (Enter=Todas): ")
            
            try:
                todas_reservas = reserva_service.listar_todas_reservas()
                if not filtro or filtro == '0':
                    print(f"\nTotal de reservas: {len(todas_reservas)}")
                    if todas_reservas:
                        mostrar_tabla_reservas(todas_reservas)
                else:
                    estado_idx = int(filtro) - 1
                    if 0 <= estado_idx < len(ESTADOS_RESERVA):
                        estado_seleccionado = ESTADOS_RESERVA[estado_idx]
                        reservas = [r for r in todas_reservas if r.estado == estado_seleccionado]
                        print(f"\nReservas en estado '{estado_seleccionado}': {len(reservas)}")
                        if reservas:
                            mostrar_tabla_reservas(reservas)
                        else:
                            print("No hay reservas en este estado.")
            except Exception as e:
                print(f"ERROR: {e}")
            pausar()
            
        elif opcion == 5:
            break


def menu_admin_reportes():
    """Dashboard rápido con estadísticas clave del sistema."""
    from src.business.pago_service import PagoService
    from src.utils.constants import ESTADOS_RESERVA
    
    reserva_service = ReservaService()
    usuario_service = UsuarioService()
    pago_service = PagoService()
    destino_service = DestinoService()
    paquete_service = PaqueteService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: DASHBOARD ===\n")
        
        try:
            # Obtener datos
            todas_reservas = reserva_service.listar_todas_reservas()
            todos_pagos = pago_service.pago_dao.listar_todos()
            todos_usuarios = usuario_service.listar_todos_usuarios()
            todos_destinos = destino_service.listar_todos_destinos_admin()
            todos_paquetes = paquete_service.listar_todos_paquetes_admin()
            
            clientes = [u for u in todos_usuarios if u.rol == 'CLIENTE']
            
            # === SECCIÓN 1: RESUMEN GENERAL ===
            print("╔════════════════════════════════════════════════════════════════╗")
            print("║                       RESUMEN GENERAL                          ║")
            print("╠════════════════════════════════════════════════════════════════╣")
            print(f"║  Total de Clientes:     {len(clientes):<35} ║")
            print(f"║  Destinos Activos:      {len([d for d in todos_destinos if d['activo']]):<35} ║")
            print(f"║  Paquetes Activos:      {len([p for p in todos_paquetes if p['activo']]):<35} ║")
            print(f"║  Total de Reservas:     {len(todas_reservas):<35} ║")
            print("╚════════════════════════════════════════════════════════════════╝")
            
            # === SECCIÓN 2: RESERVAS POR ESTADO ===
            print("\n╔════════════════════════════════════════════════════════════════╗")
            print("║                     RESERVAS POR ESTADO                        ║")
            print("╠════════════════════════════════════════════════════════════════╣")
            for estado in ESTADOS_RESERVA:
                count = len([r for r in todas_reservas if r.estado == estado])
                barra = "█" * min(count, 20)
                print(f"║  {estado:<12}: {count:>3} {barra:<20}                  ║")
            print("╚════════════════════════════════════════════════════════════════╝")
            
            # === SECCIÓN 3: INGRESOS ===
            pagos_completados = [p for p in todos_pagos if p.estado == 'COMPLETADO']
            total_ingresos = sum(p.monto for p in pagos_completados)
            print("\n╔════════════════════════════════════════════════════════════════╗")
            print("║                       INGRESOS                                 ║")
            print("╠════════════════════════════════════════════════════════════════╣")
            print(f"║  Pagos Completados:        {len(pagos_completados):<35} ║")
            total_formateado = f"${int(total_ingresos):,}".replace(",", ".")
            print(f"║  Total Recaudado:          {total_formateado:<35} ║")
            print("╚════════════════════════════════════════════════════════════════╝")
            
            # === SECCIÓN 4: TOP 3 DESTINOS ===
            print("\n╔════════════════════════════════════════════════════════════════╗")
            print("║                    TOP DESTINOS (por reservas)                 ║")
            print("╠════════════════════════════════════════════════════════════════╣")
            
            # Contar reservas por destino
            destino_counts = {}
            for r in todas_reservas:
                if r.destino_id:
                    destino_counts[r.destino_id] = destino_counts.get(r.destino_id, 0) + 1
            
            # Ordenar y mostrar top 3
            top_destinos = sorted(destino_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            if top_destinos:
                for i, (destino_id, count) in enumerate(top_destinos, 1):
                    destino = next((d for d in todos_destinos if d['id'] == destino_id), None)
                    nombre = destino['nombre'][:30] if destino else "Desconocido"
                    print(f"║  {i}. {nombre:<35} ({count} reservas)     ║")
            else:
                print("║  No hay reservas de destinos aún                               ║")
            print("╚════════════════════════════════════════════════════════════════╝")
            
        except Exception as e:
            print(f"ERROR al cargar dashboard: {e}")
        
        print("\n1. Actualizar Dashboard")
        print("2. Volver")
        opcion = leer_opcion()
        if opcion == 2:
            break


def menu_admin_politicas():
    """Muestra las políticas de cancelación fijas del sistema.
    
    Las políticas son subclases fijas (PoliticaFlexible, PoliticaEstricta) 
    y no se pueden crear/editar/eliminar desde el menú.
    """
    from src.business.politica_cancelacion_service import PoliticaCancelacionService
    
    politica_service = PoliticaCancelacionService()
    
    limpiar_pantalla()
    print("=== VIAJES AVENTURA: POLÍTICAS DE CANCELACIÓN ===\n")
    print("Las políticas de cancelación son tipos fijos del sistema:")
    print("(Basadas en herencia de clases - no modificables)\n")
    
    try:
        politicas = politica_service.listar_todas_politicas()
        if not politicas:
            print("No hay políticas registradas en la base de datos.")
        else:
            print("="*70)
            print(" POLÍTICAS DISPONIBLES".center(70))
            print("="*70)
            for p in politicas:
                print(f"  {p.id}. {p.nombre}")
                print(f"     -> {p.dias_aviso} días de aviso, {p.porcentaje_reembolso}% reembolso")
                print()
            print("="*70)
            
            print("\nEstas políticas se asignan a Destinos y Paquetes al crearlos/editarlos.")
            print("Cada política tiene su propia lógica de cálculo de reembolso (herencia).")
    except Exception as e:
        print(f"ERROR al cargar políticas: {e}")
    
    pausar()

