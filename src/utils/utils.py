import os


class OperacionCancelada(Exception):
    """Excepción lanzada cuando el usuario cancela una operación."""
    pass


def validar_cancelacion(valor: str) -> str:
    """Verifica si el usuario desea cancelar. Si es así, lanza OperacionCancelada.
    
    Args:
        valor: String ingresado por el usuario
        
    Returns:
        El valor original si no es cancelación
        
    Raises:
        OperacionCancelada: Si el valor es '0', 'cancelar', 'cancel' o vacío (Enter)
    """
    valor_limpio = valor.strip()
    if valor_limpio.lower() in ['0', 'cancelar', 'cancel', '']:
        raise OperacionCancelada("Operación cancelada por el usuario")
    return valor


def validar_opcion(opcion:int, min:int, max:int) -> bool:
    #Valida entrada del usuario
    if not isinstance(opcion,int) and not isinstance(min,int) and not isinstance(max,int):
        print("La opción y los minimos y máximos deben ser numeros.")
        return False
    return min <= opcion <= max

def limpiar_pantalla():
    #Limpia la consola
    os.system("cls")

def pausar():
    #Espera input del usuario antes de continuar
    input("Presione Enter para continuar...")

def mostrar_tabla_paquetes(paquetes: list) -> None:
    """Muestra lista de paquetes con descripción completa."""
    if not paquetes:
        print("No hay paquetes para mostrar.")
        return
    
    print("\n" + "="*100)
    for p in paquetes:
        precio = f"${int(p.precio_total):,}".replace(",", ".")
        fecha_inicio = str(p.fecha_inicio)[:16] if p.fecha_inicio else "N/A"
        fecha_fin = str(p.fecha_fin)[:16] if p.fecha_fin else "N/A"
        
        print(f"\nID: {p.id}")
        print(f"NOMBRE: {p.nombre}")
        print(f"PRECIO: {precio}")
        print(f"CUPOS DISPONIBLES: {p.cupos_disponibles}")
        print(f"INICIO: {fecha_inicio}")
        print(f"FIN: {fecha_fin}")
        print(f"DESCRIPCIÓN: {p.descripcion or 'Sin descripción'}")
        print("-"*100)
    print("="*100 + "\n")

def mostrar_tabla_destinos(destinos: list) -> None:
    """Muestra lista de destinos en formato tabla con descripción completa."""
    if not destinos:
        print("No hay destinos para mostrar.")
        return
    
    # Mostrar cada destino en su propio bloque
    print("\n" + "="*100)
    for d in destinos:
        costo = f"${int(d.costo_base):,}".replace(",", ".")
        print(f"\nID: {d.id}")
        print(f"NOMBRE: {d.nombre}")
        print(f"COSTO BASE: {costo}")
        print(f"CUPOS DISPONIBLES: {d.cupos_disponibles}")
        print(f"DESCRIPCIÓN: {d.descripcion}")
        print("-"*100)
    print("="*100 + "\n")

def mostrar_tabla_actividades(actividades: list) -> None:
    """Muestra lista de actividades en formato tabla."""
    if not actividades:
        print("No hay actividades para mostrar.")
        return
    
    print("\n" + "="*110)
    print(f"{'ID':<5} {'NOMBRE':<35} {'DURACIÓN':<12} {'PRECIO':<12} {'DESTINO ID':<12} {'DESCRIPCIÓN':<32}")
    print("="*110)
    
    for a in actividades:
        duracion = f"{a.duracion_horas}h"
        precio = f"${int(a.precio_base):,}".replace(",", ".")
        descripcion = (a.descripcion[:29] + "...") if a.descripcion and len(a.descripcion) > 29 else (a.descripcion or "")
        print(f"{a.id:<5} {a.nombre:<35} {duracion:<12} {precio:<12} {a.destino_id:<12} {descripcion:<32}")
    
    print("="*110 + "\n")

def mostrar_tabla_reservas(reservas: list) -> None:
    """Muestra lista de reservas en formato tabla."""
    from src.dao.destino_dao import DestinoDAO
    from src.dao.paquete_dao import PaqueteDAO
    
    if not reservas:
        print("No hay reservas para mostrar.")
        return
    
    paquete_dao = PaqueteDAO()
    destino_dao = DestinoDAO()
    
    print("\n" + "="*110)
    print(f"{'ID':<5} {'TIPO':<12} {'ESTADO':<12} {'PERSONAS':<10} {'MONTO':<14} {'FECHA':<20} {'NOMBRE':<37}")
    print("="*110)
    
    for r in reservas:
        monto = f"${int(r.monto_total):,}".replace(",", ".")
        fecha = str(r.fecha_reserva)[:19] if r.fecha_reserva else "N/A"
        
        # Determinar tipo y nombre según sea paquete o destino
        if r.paquete_id:
            tipo = "Paquete"
            paquete = paquete_dao.obtener_por_id(r.paquete_id)
            nombre = paquete.nombre if paquete else f"Paquete #{r.paquete_id}"
        elif r.destino_id:
            tipo = "Destino"
            destino = destino_dao.obtener_por_id(r.destino_id)
            nombre = destino.nombre if destino else f"Destino #{r.destino_id}"
        else:
            tipo = "Desconocido"
            nombre = "N/A"
        
        # Truncar nombre si es muy largo
        nombre = (nombre[:34] + "...") if len(nombre) > 34 else nombre
        
        print(f"{r.id:<5} {tipo:<12} {r.estado:<12} {r.numero_personas:<10} {monto:<14} {fecha:<20} {nombre:<37}")
    
    print("="*110 + "\n")

def mostrar_tabla_pagos(pagos: list) -> None:
    """Muestra lista de pagos en formato tabla."""
    from src.dao.destino_dao import DestinoDAO
    from src.dao.paquete_dao import PaqueteDAO
    from src.dao.reserva_dao import ReservaDAO
    
    if not pagos:
        print("No hay pagos para mostrar.")
        return
    
    reserva_dao = ReservaDAO()
    paquete_dao = PaqueteDAO()
    destino_dao = DestinoDAO()
    
    print("\n" + "="*120)
    print(f"{'ID':<5} {'RESERVA':<40} {'MONTO':<12} {'MÉTODO':<15} {'ESTADO':<12} {'FECHA':<20}")
    print("="*120)
    
    for p in pagos:
        monto = f"${int(p.monto):,}".replace(",", ".")
        fecha = str(p.fecha_pago)[:19] if p.fecha_pago else "N/A"
        
        # Obtener información de la reserva
        reserva = reserva_dao.obtener_por_id(p.reserva_id)
        if reserva:
            if reserva.paquete_id:
                paquete = paquete_dao.obtener_por_id(reserva.paquete_id)
                reserva_info = f"Reserva #{p.reserva_id} - Paquete: {paquete.nombre if paquete else 'N/A'}"
            elif reserva.destino_id:
                destino = destino_dao.obtener_por_id(reserva.destino_id)
                reserva_info = f"Reserva #{p.reserva_id} - Destino: {destino.nombre if destino else 'N/A'}"
            else:
                reserva_info = f"Reserva #{p.reserva_id}"
        else:
            reserva_info = f"Reserva #{p.reserva_id}"
        
        # Truncar si es muy largo
        reserva_info = (reserva_info[:37] + "...") if len(reserva_info) > 37 else reserva_info
        
        print(f"{p.id:<5} {reserva_info:<40} {monto:<12} {p.metodo:<15} {p.estado:<12} {fecha:<20}")
    
    print("="*120 + "\n")


def mostrar_actividades_paquete(actividades: list) -> None:
    """Muestra las actividades incluidas en un paquete."""
    if not actividades:
        print("\n  Este paquete no tiene actividades asignadas.\n")
        return
    
    print("\n  ACTIVIDADES INCLUIDAS:")
    print("  " + "-"*90)
    destino_actual = None
    for act in actividades:
        # Agrupar por destino
        if act['destino_nombre'] != destino_actual:
            destino_actual = act['destino_nombre']
            print(f"\n  📍 {destino_actual}")
        
        print(f"     • {act['nombre']} ({act['duracion_horas']}h)")
        if act.get('descripcion'):
            print(f"       {act['descripcion']}")
    print("  " + "-"*90 + "\n")