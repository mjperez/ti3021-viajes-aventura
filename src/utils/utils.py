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
    """Muestra lista de paquetes en formato tabla."""
    if not paquetes:
        print("No hay paquetes para mostrar.")
        return
    
    # Encabezado
    print("\n" + "="*120)
    print(f"{'ID':<5} {'NOMBRE':<30} {'PRECIO':<12} {'CUPOS':<8} {'FECHA INICIO':<20} {'FECHA FIN':<20}")
    print("="*120)
    
    # Filas
    for p in paquetes:
        precio = f"${p.precio_total:,.2f}"
        fecha_inicio = str(p.fecha_inicio)[:16] if p.fecha_inicio else "N/A"
        fecha_fin = str(p.fecha_fin)[:16] if p.fecha_fin else "N/A"
        print(f"{p.id:<5} {p.nombre:<30} {precio:<12} {p.cupos_disponibles:<8} {fecha_inicio:<20} {fecha_fin:<20}")
    
    print("="*120 + "\n")

def mostrar_tabla_destinos(destinos: list) -> None:
    """Muestra lista de destinos en formato tabla."""
    if not destinos:
        print("No hay destinos para mostrar.")
        return
    
    print("\n" + "="*100)
    print(f"{'ID':<5} {'NOMBRE':<30} {'COSTO BASE':<15} {'DESCRIPCIÓN':<48}")
    print("="*100)
    
    for d in destinos:
        costo = f"${d.costo_base:,.2f}"
        descripcion = d.descripcion[:45] + "..." if len(d.descripcion) > 45 else d.descripcion
        print(f"{d.id:<5} {d.nombre:<30} {costo:<15} {descripcion:<48}")
    
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
        precio = f"${a.precio_base:,.2f}"
        descripcion = (a.descripcion[:29] + "...") if a.descripcion and len(a.descripcion) > 29 else (a.descripcion or "")
        print(f"{a.id:<5} {a.nombre:<35} {duracion:<12} {precio:<12} {a.destino_id:<12} {descripcion:<32}")
    
    print("="*110 + "\n")

def mostrar_tabla_reservas(reservas: list) -> None:
    """Muestra lista de reservas en formato tabla."""
    if not reservas:
        print("No hay reservas para mostrar.")
        return
    
    print("\n" + "="*110)
    print(f"{'ID':<5} {'PAQUETE ID':<12} {'ESTADO':<12} {'PERSONAS':<10} {'MONTO':<12} {'FECHA':<20} {'USUARIO ID':<12}")
    print("="*110)
    
    for r in reservas:
        monto = f"${r.monto_total:,.2f}"
        fecha = str(r.fecha_reserva)[:19] if r.fecha_reserva else "N/A"
        print(f"{r.id:<5} {r.paquete_id:<12} {r.estado:<12} {r.numero_personas:<10} {monto:<12} {fecha:<20} {r.usuario_id:<12}")
    
    print("="*110 + "\n")

def mostrar_tabla_pagos(pagos: list) -> None:
    """Muestra lista de pagos en formato tabla."""
    if not pagos:
        print("No hay pagos para mostrar.")
        return
    
    print("\n" + "="*100)
    print(f"{'ID':<5} {'RESERVA ID':<12} {'MONTO':<12} {'MÉTODO':<15} {'ESTADO':<12} {'FECHA':<20}")
    print("="*100)
    
    for p in pagos:
        monto = f"${p.monto:,.2f}"
        fecha = str(p.fecha_pago)[:19] if p.fecha_pago else "N/A"
        print(f"{p.id:<5} {p.reserva_id:<12} {monto:<12} {p.metodo:<15} {p.estado:<12} {fecha:<20}")
    
    print("="*100 + "\n")