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


def leer_opcion(prompt: str = "Elija su opción: ") -> int:
    """Lee una opción numérica del usuario, devolviendo -1 si es inválida."""
    try:
        valor = input(prompt).strip()
        if not valor:
            return -1
        return int(valor)
    except ValueError:
        return -1


def leer_entero(prompt: str, valor_cancelar: int = 0) -> int | None:
    """Lee un número entero del usuario.
    
    Returns:
        El número ingresado, o None si el usuario cancela o ingresa valor inválido.
    """
    try:
        valor = input(prompt).strip()
        if not valor or int(valor) == valor_cancelar:
            return None
        return int(valor)
    except ValueError:
        print("Error: Debe ingresar un número válido.")
        return None


def limpiar_pantalla():
    #Limpia la consola
    os.system("cls")

def pausar():
    #Espera input del usuario antes de continuar
    input("Presione Enter para continuar...")

def mostrar_tabla_paquetes(paquetes: list) -> None:
    """Muestra lista de paquetes en formato tabla."""
    from src.business.paquete_service import PaqueteService
    
    if not paquetes:
        print("No hay paquetes para mostrar.")
        return
    
    paquete_service = PaqueteService()
    
    # Encabezado
    print("\n" + "="*120)
    print(f"{'ID':<5} {'NOMBRE':<35} {'PRECIO':<15} {'CUPOS':<8} {'FECHA INICIO':<12} {'FECHA FIN':<12}")
    print("="*120)
    
    for p in paquetes:
        precio = f"${int(p.precio_total):,}".replace(",", ".")
        fecha_inicio = str(p.fecha_inicio)[:10] if p.fecha_inicio else "N/A"
        fecha_fin = str(p.fecha_fin)[:10] if p.fecha_fin else "N/A"
        nombre = (p.nombre[:32] + "...") if len(p.nombre) > 35 else p.nombre
        
        print(f"{p.id:<5} {nombre:<35} {precio:<15} {p.cupos_disponibles:<8} {fecha_inicio:<12} {fecha_fin:<12}")
        
        # Mostrar actividades incluidas en el paquete
        if p.id:
            actividades = paquete_service.obtener_actividades_paquete(p.id)
            if actividades:
                print("      └─ Actividades: ", end="")
                acts_str = ", ".join([f"{a['nombre']} ({a['duracion_horas']}h)" for a in actividades[:3]])
                if len(actividades) > 3:
                    acts_str += f" +{len(actividades)-3} más"
                print(acts_str)
        print("-"*120)
    print("="*120 + "\n")

def mostrar_tabla_destinos(destinos: list) -> None:
    """Muestra lista de destinos en formato tabla con política de cancelación."""
    if not destinos:
        print("No hay destinos para mostrar.")
        return
    
    # Obtener políticas para mostrar nombre
    from src.dao.politica_cancelacion_dao import PoliticaCancelacionDAO
    politica_dao = PoliticaCancelacionDAO()
    politicas = {p.id: p.nombre for p in politica_dao.listar_todas()}
    
    # Encabezado
    print("\n" + "="*125)
    print(f"{'ID':<5} {'NOMBRE':<25} {'COSTO BASE':<15} {'CUPOS':<8} {'POLÍTICA':<12} {'DESCRIPCIÓN':<50}")
    print("="*125)
    
    for d in destinos:
        costo = f"${int(d.costo_base):,}".replace(",", ".")
        descripcion = (d.descripcion[:47] + "...") if len(d.descripcion) > 50 else d.descripcion
        politica_nombre = politicas.get(d.politica_id, "Flexible")
        print(f"{d.id:<5} {d.nombre:<25} {costo:<15} {d.cupos_disponibles:<8} {politica_nombre:<12} {descripcion:<50}")
    
    print("="*125 + "\n")

def mostrar_tabla_actividades(actividades: list) -> None:
    """Muestra lista de actividades en formato tabla."""
    if not actividades:
        print("No hay actividades para mostrar.")
        return
    
    # Encabezado
    print("\n" + "="*115)
    print(f"{'ID':<5} {'NOMBRE':<30} {'DURACIÓN':<10} {'PRECIO':<15} {'DESTINO':<8} {'DESCRIPCIÓN':<40}")
    print("="*115)
    
    for a in actividades:
        duracion = f"{a.duracion_horas}h"
        precio = f"${int(a.precio_base):,}".replace(",", ".")
        descripcion = (a.descripcion[:37] + "...") if a.descripcion and len(a.descripcion) > 40 else (a.descripcion or "Sin descripción")
        nombre = (a.nombre[:27] + "...") if len(a.nombre) > 30 else a.nombre
        
        print(f"{a.id:<5} {nombre:<30} {duracion:<10} {precio:<15} {a.destino_id:<8} {descripcion:<40}")
    
    print("="*115 + "\n")

def mostrar_tabla_reservas(reservas: list) -> None:
    """Muestra lista de reservas en formato tabla con información del cliente."""
    from src.dao.destino_dao import DestinoDAO
    from src.dao.paquete_dao import PaqueteDAO
    from src.dao.usuario_dao import UsuarioDAO
    
    if not reservas:
        print("No hay reservas para mostrar.")
        return
    
    paquete_dao = PaqueteDAO()
    destino_dao = DestinoDAO()
    usuario_dao = UsuarioDAO()
    
    # Encabezado
    print("\n" + "="*140)
    print(f"{'ID':<5} {'CLIENTE':<20} {'TIPO':<10} {'NOMBRE':<25} {'ESTADO':<12} {'PERS':<6} {'MONTO':<15} {'FECHA':<20}")
    print("="*140)
    
    for r in reservas:
        monto = f"${int(r.monto_total):,}".replace(",", ".")
        fecha = str(r.fecha_reserva)[:16] if r.fecha_reserva else "N/A"
        
        # Obtener nombre del cliente
        usuario = usuario_dao.obtener_por_id(r.usuario_id)
        cliente = usuario.nombre if usuario else f"Usuario #{r.usuario_id}"
        cliente = (cliente[:17] + "...") if len(cliente) > 20 else cliente
        
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
            tipo = "N/A"
            nombre = "N/A"
        
        nombre = (nombre[:22] + "...") if len(nombre) > 25 else nombre
        print(f"{r.id:<5} {cliente:<20} {tipo:<10} {nombre:<25} {r.estado:<12} {r.numero_personas:<6} {monto:<15} {fecha:<20}")
    
    print("="*140 + "\n")

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
    
    # Encabezado
    print("\n" + "="*120)
    print(f"{'ID':<5} {'RES.ID':<8} {'TIPO':<10} {'NOMBRE':<25} {'MONTO':<15} {'MÉTODO':<15} {'ESTADO':<12} {'FECHA':<18}")
    print("="*120)
    
    for p in pagos:
        monto = f"${int(p.monto):,}".replace(",", ".")
        fecha = str(p.fecha_pago)[:16] if p.fecha_pago else "N/A"
        
        # Obtener información de la reserva
        reserva = reserva_dao.obtener_por_id(p.reserva_id)
        if reserva:
            if reserva.paquete_id:
                paquete = paquete_dao.obtener_por_id(reserva.paquete_id)
                reserva_tipo = "Paquete"
                reserva_nombre = paquete.nombre if paquete else 'N/A'
            elif reserva.destino_id:
                destino = destino_dao.obtener_por_id(reserva.destino_id)
                reserva_tipo = "Destino"
                reserva_nombre = destino.nombre if destino else 'N/A'
            else:
                reserva_tipo = "N/A"
                reserva_nombre = "N/A"
        else:
            reserva_tipo = "N/A"
            reserva_nombre = "N/A"
        
        reserva_nombre = (reserva_nombre[:22] + "...") if len(reserva_nombre) > 25 else reserva_nombre
        print(f"{p.id:<5} {p.reserva_id:<8} {reserva_tipo:<10} {reserva_nombre:<25} {monto:<15} {p.metodo:<15} {p.estado:<12} {fecha:<18}")
    
    print("="*120 + "\n")


def mostrar_actividades_paquete(actividades: list) -> None:
    """Muestra las actividades incluidas en un paquete en formato compacto."""
    if not actividades:
        return
    
    # Agrupar por destino
    destinos = {}
    for act in actividades:
        dest = act['destino_nombre']
        if dest not in destinos:
            destinos[dest] = []
        destinos[dest].append(act)
    
    for destino, acts in destinos.items():
        acts_str = ", ".join([f"{a['nombre']} ({a['duracion_horas']}h - ${int(a.get('precio_base', 0)):,}".replace(",", ".") + ")" for a in acts])
        print(f"      📍 {destino}: {acts_str}")