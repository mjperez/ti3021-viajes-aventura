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
        print("4. Eliminar Destino")
        print("5. Volver")
        opcion = leer_opcion()
        
        if not validar_opcion(opcion, 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
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
        elif opcion == 2:
            print("=== VIAJES AVENTURA: AGREGAR DESTINO ===")
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
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
                politica_str = input("Seleccione política (Enter=1 Flexible): ") or "1"
                politica_id = int(politica_str) if politica_str in ["1", "2"] else 1
                
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
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
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
                nuevo_costo_base_str = input(f"Nuevo costo base (Enter para mantener '{destino.costo_base}'): ")
                nuevo_costo_base = float(nuevo_costo_base_str) if nuevo_costo_base_str else destino.costo_base
                nuevos_cupos_str = input(f"Nuevos cupos (Enter para mantener '{destino.cupos_disponibles}'): ")
                nuevos_cupos = int(nuevos_cupos_str) if nuevos_cupos_str else destino.cupos_disponibles
                
                # Opción de cambiar política
                print("\nPolíticas de cancelación:")
                print("  1. Flexible (3 días aviso, 100% reembolso)")
                print("  2. Estricta (7 días aviso, 50% reembolso)")
                nueva_politica_str = input(f"Nueva política (Enter para mantener '{politica_actual}'): ")
                nueva_politica_id = int(nueva_politica_str) if nueva_politica_str in ["1", "2"] else destino.politica_id
                
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
            print("=== VIAJES AVENTURA: ELIMINAR DESTINO ===")
            destinos = destino_service.listar_todos_destinos()
            if destinos:
                print("Destinos disponibles:")
                mostrar_tabla_destinos(destinos)
            else:
                print("No hay destinos registrados.")
                pausar()
                continue
            id_eliminar = int(input("\nIngrese el ID del destino a eliminar: "))
            destino = destino_service.obtener_destino(id_eliminar)
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
                eliminado = destino_service.eliminar_destino(id_eliminar)
                if eliminado:
                    print(f"Destino ID {id_eliminar} eliminado exitosamente.")
                else:
                    print(f"No se pudo eliminar el destino ID {id_eliminar}.")
            except Exception as e:
                print(f"Error al eliminar destino: {e}")
      
            pausar()
        elif opcion == 5:
            break


def menu_admin_actividades():
    """Submenú para gestión de actividades."""
    actividad_service = ActividadService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: ACTIVIDADES ===")
        print("1. Listar Actividades")
        print("2. Agregar Actividad")
        print("3. Editar Actividad")
        print("4. Eliminar Actividad")
        print("5. Volver")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
            print("=== VIAJES AVENTURA: LISTAR ACTIVIDADES ===")
            actividades = actividad_service.listar_todas_actividades()
            if not actividades:
                print("No hay actividades registradas.")
            else:
                mostrar_tabla_actividades(actividades)
            pausar()
        elif opcion == 2:
            print("=== VIAJES AVENTURA: AGREGAR ACTIVIDAD ===")
            print("(Escriba 'cancelar' para abortar)\n")
            
            # Listar PAQUETES disponibles PRIMERO (cambio de flujo solicitado)
            # Aunque la actividad pertenece al destino, el usuario piensa en Paquetes.
            paquete_service = PaqueteService()
            paquetes = paquete_service.listar_todos_paquetes()
            
            if not paquetes:
                print("No hay paquetes disponibles. Cree paquetes primero.")
                print("(O use el menú de Destinos si desea asociar directamente a uno sin paquete)")
                pausar()
                continue
                
            print("Paquetes disponibles:")
            mostrar_tabla_paquetes(paquetes)
            
            try:
                # Elegir paquete
                paquete_id_str = input("\nID del paquete al que pertenece la actividad (o 'cancelar'): ")
                if paquete_id_str.lower() == 'cancelar':
                    print("\nINFO: Operación cancelada.")
                    pausar()
                    continue
                paquete_id = int(paquete_id_str)
                
                # Obtener destinos del paquete
                destinos_paquete = paquete_service.obtener_destinos_paquete(paquete_id)
                
                if not destinos_paquete:
                    print(f"ERROR: El paquete ID {paquete_id} no tiene destinos asociados.")
                    print("Asocie destinos al paquete antes de crear actividades.")
                    pausar()
                    continue
                
                # Determinar destino_id
                destino_id = 0
                if len(destinos_paquete) == 1:
                    destino_id = destinos_paquete[0]['id']
                    print(f"Asociando automáticamente al destino: {destinos_paquete[0]['nombre']}")
                else:
                    print("\nEste paquete tiene múltiples destinos. Seleccione a cuál corresponde la actividad:")
                    print("="*60)
                    for d in destinos_paquete:
                        print(f" ID {d['id']}: {d['nombre']}")
                    print("="*60)
                    
                    while True:
                        dest_input = input("ID del destino: ")
                        if not dest_input:
                            continue
                        try: 
                            d_id = int(dest_input)
                            # Validar que sea uno de la lista
                            if any(d['id'] == d_id for d in destinos_paquete):
                                destino_id = d_id
                                break
                            else:
                                print("Error: Seleccione un ID de la lista mostrada.")
                        except ValueError:
                            print("Error: Ingrese un número válido.")

                nombre = input("\nNombre de la actividad: ")
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
                print(f"(Vinculada al destino ID {destino_id}, visible en el paquete)")
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
            print("=== VIAJES AVENTURA: ELIMINAR ACTIVIDAD ===")
            try:
                actividades = actividad_service.listar_todas_actividades()
                if not actividades:
                    print("No hay actividades registradas.")
                else:
                    mostrar_tabla_actividades(actividades)
                id_eliminar = int(input("\nID de la actividad a eliminar: "))
                actividad = actividad_service.obtener_actividad(id_eliminar)
                if not actividad:
                    print(f"No se encontró actividad con ID {id_eliminar}")
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
                    print("Eliminación cancelada")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif opcion == 5:
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
        print("4. Eliminar Paquete")
        print("5. Volver")
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 5):
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
                fecha_inicio_str = input("Fecha inicio (YYYY-MM-DD): ")
                fecha_fin_str = input("Fecha fin (YYYY-MM-DD): ")
                precio = float(input("Precio total: "))
                cupos = int(input("Cupos disponíveis: "))
                politica_id = int(input("ID política de cancelación (ej: 1): "))
                
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d")
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d")
                
                nuevo_paquete = paquete_service.crear_paquete(
                    nombre=nombre,
                    descripcion="",
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
        elif opcion == 4:
            print("=== VIAJES AVENTURA: ELIMINAR PAQUETE ===")
            try:
                paquetes = paquete_service.listar_todos_paquetes()
                if not paquetes:
                    print("No hay paquetes registrados.")
                else:
                    mostrar_tabla_paquetes(paquetes)                
                id_eliminar = int(input("\nID del paquete a eliminar: "))
                paquete = paquete_service.obtener_paquete(id_eliminar)
                if not paquete:
                    print(f"No se encontró paquete con ID {id_eliminar}")
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
                    print("Eliminación cancelada")
            except Exception as e:
                print(f"ERROR: Error: {e}")
            pausar()
        elif opcion == 5:
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
        opcion = leer_opcion()
        if not validar_opcion(opcion, 1, 4):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
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
        elif opcion == 2:
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
        elif opcion == 3:
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
        elif opcion == 4:
            break


def menu_admin_politicas():
    """Submenú para gestión completa de políticas de cancelación."""
    from src.business.politica_cancelacion_service import PoliticaCancelacionService
    
    politica_service = PoliticaCancelacionService()
    
    while True:
        limpiar_pantalla()
        print("=== VIAJES AVENTURA: POLÍTICAS DE CANCELACIÓN ===")
        print("1. Listar Políticas")
        print("2. Agregar Política")
        print("3. Editar Política")
        print("4. Eliminar Política")
        print("5. Volver")
        opcion = leer_opcion()
        
        if not validar_opcion(opcion, 1, 5):
            print(MSG_ERROR_OPCION_INVALIDA)
            pausar()
            continue
        limpiar_pantalla()
        if opcion == 1:
            print("=== VIAJES AVENTURA: LISTAR POLÍTICAS ===\n")
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
            except Exception as e:
                print(f"ERROR: Error al cargar políticas: {e}")
            pausar()
            
        elif opcion == 2:
            print("=== VIAJES AVENTURA: AGREGAR POLÍTICA ===")
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
            try:
                nombre = validar_cancelacion(input("Nombre de la política: "))
                dias_aviso_str = validar_cancelacion(input("Días de aviso requeridos (0-365): "))
                dias_aviso = int(dias_aviso_str)
                porcentaje_str = validar_cancelacion(input("Porcentaje de reembolso (0-100): "))
                porcentaje_reembolso = float(porcentaje_str)
                
                nueva_politica = politica_service.crear_politica(nombre, dias_aviso, porcentaje_reembolso)
                print(f"\nEXITO: Política '{nueva_politica.nombre}' creada con ID: {nueva_politica.id}")
            except OperacionCancelada:
                print("\nINFO: Operación cancelada.")
            except Exception as e:
                print(f"\nERROR: {e}")
            pausar()
            
        elif opcion == 3:
            print("=== VIAJES AVENTURA: EDITAR POLÍTICA ===")
            print("(Presione Enter, '0' o 'cancelar' para abortar)\n")
            try:
                # Mostrar políticas disponibles
                politicas = politica_service.listar_todas_politicas()
                if not politicas:
                    print("No hay políticas para editar.")
                    pausar()
                    continue
                    
                print("Políticas disponibles:")
                for p in politicas:
                    print(f"  ID {p.id}: {p.nombre} ({p.dias_aviso} días, {p.porcentaje_reembolso}% reembolso)")
                
                id_editar_str = validar_cancelacion(input("\nIngrese ID de la política a editar: "))
                id_editar = int(id_editar_str)
                
                politica = politica_service.obtener_politica(id_editar)
                if not politica:
                    print(f"\nERROR: No se encontró política con ID {id_editar}")
                    pausar()
                    continue
                
                print(f"\nPolítica actual: {politica.nombre}")
                nuevo_nombre = input(f"Nuevo nombre (Enter para mantener '{politica.nombre}'): ") or politica.nombre
                nuevos_dias_str = input(f"Nuevos días de aviso (Enter para mantener {politica.dias_aviso}): ")
                nuevos_dias = int(nuevos_dias_str) if nuevos_dias_str else politica.dias_aviso
                nuevo_porcentaje_str = input(f"Nuevo % reembolso (Enter para mantener {politica.porcentaje_reembolso}): ")
                nuevo_porcentaje = float(nuevo_porcentaje_str) if nuevo_porcentaje_str else politica.porcentaje_reembolso
                
                politica_actualizada = politica_service.actualizar_politica(
                    id_editar, nuevo_nombre, nuevos_dias, nuevo_porcentaje
                )
                print(f"\nEXITO: Política '{politica_actualizada.nombre}' actualizada correctamente.")
            except OperacionCancelada:
                print("\nINFO: Operación cancelada.")
            except Exception as e:
                print(f"\nERROR: {e}")
            pausar()
            
        elif opcion == 4:
            print("=== VIAJES AVENTURA: ELIMINAR POLÍTICA ===")
            try:
                # Mostrar políticas disponibles
                politicas = politica_service.listar_todas_politicas()
                if not politicas:
                    print("No hay políticas para eliminar.")
                    pausar()
                    continue
                    
                print("Políticas disponibles:")
                for p in politicas:
                    print(f"  ID {p.id}: {p.nombre}")
                
                id_eliminar = int(input("\nIngrese ID de la política a eliminar (0 para cancelar): "))
                if id_eliminar == 0:
                    continue
                
                politica = politica_service.obtener_politica(id_eliminar)
                if not politica:
                    print(f"\nERROR: No se encontró política con ID {id_eliminar}")
                    pausar()
                    continue
                
                print(f"\nPolítica a eliminar: {politica.nombre}")
                confirmar = input("¿Está seguro? (s/n): ")
                if confirmar.lower() != 's':
                    print("Eliminación cancelada.")
                    pausar()
                    continue
                
                if politica_service.eliminar_politica(id_eliminar):
                    print(f"\nEXITO: Política '{politica.nombre}' eliminada correctamente.")
                else:
                    print("\nERROR: No se pudo eliminar la política.")
            except Exception as e:
                print(f"\nERROR: {e}")
            pausar()
            
        elif opcion == 5:
            break
