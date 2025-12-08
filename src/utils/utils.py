import math
import os
import re


class OperacionCancelada(Exception):
    """Excepción lanzada cuando el usuario cancela una operación."""
    pass


def sanitizar_numero(valor: str) -> str:
    """Limpia un string para convertirlo a número.
    
    Elimina puntos de miles, espacios, y símbolos de moneda.
    Reemplaza coma decimal por punto.
    
    Args:
        valor: String con el número a limpiar
        
    Returns:
        String limpio listo para convertir a int/float
    """
    if not valor:
        return "0"
    # Eliminar espacios, símbolo $, puntos de miles
    limpio = valor.strip().replace("$", "").replace(" ", "")
    # Si tiene coma como decimal (formato chileno), reemplazar
    if "," in limpio and "." in limpio:
        # Formato 1.234,56 -> 1234.56
        limpio = limpio.replace(".", "").replace(",", ".")
    elif "," in limpio:
        # Solo coma -> es decimal
        limpio = limpio.replace(",", ".")
    elif limpio.count(".") > 1:
        # Múltiples puntos = separador de miles
        limpio = limpio.replace(".", "")
    return limpio


def leer_entero_seguro(prompt: str, minimo: int | None = None, maximo: int | None = None) -> int | None:
    """Lee un entero del usuario con sanitización.
    
    Args:
        prompt: Mensaje a mostrar
        minimo: Valor mínimo permitido (opcional)
        maximo: Valor máximo permitido (opcional)
        
    Returns:
        Entero válido o None si cancela/inválido
    """
    try:
        valor = input(prompt).strip()
        if not valor or valor.lower() in ['0', 'cancelar', 'cancel']:
            return None
        
        numero = int(sanitizar_numero(valor))
        
        if minimo is not None and numero < minimo:
            print(f"Error: El valor debe ser al menos {minimo}")
            return None
        if maximo is not None and numero > maximo:
            print(f"Error: El valor no puede ser mayor a {maximo}")
            return None
            
        return numero
    except ValueError:
        print("Error: Debe ingresar un número válido (sin letras ni símbolos)")
        return None


def leer_decimal_seguro(prompt: str, minimo: float | None = None) -> float | None:
    """Lee un decimal del usuario con sanitización.
    
    Args:
        prompt: Mensaje a mostrar
        minimo: Valor mínimo permitido (opcional)
        
    Returns:
        Float válido o None si cancela/inválido
    """
    try:
        valor = input(prompt).strip()
        if not valor or valor.lower() in ['0', 'cancelar', 'cancel']:
            return None
        
        numero = float(sanitizar_numero(valor))
        
        if minimo is not None and numero < minimo:
            print(f"Error: El valor debe ser al menos {minimo}")
            return None
            
        return numero
    except ValueError:
        print("Error: Debe ingresar un número válido (sin letras)")
        return None


def calcular_precio_con_iva(precio_base: int | float, iva: float = 0.19) -> int:
    """Calcula el precio total incluyendo IVA, redondeando al techo.
    
    En Chile no existen decimales en la moneda, por lo que se redondea
    hacia arriba (ceil) para no perder centavos.
    
    Args:
        precio_base: Precio sin IVA (entero o float)
        iva: Tasa de IVA (default 19%)
        
    Returns:
        Precio con IVA incluido, redondeado al entero superior
    """
    return math.ceil(precio_base * (1 + iva))


def formatear_precio(precio: int | float, con_iva: bool = False) -> str:
    """Formatea un precio en formato chileno con símbolo $.
    
    Args:
        precio: Monto a formatear
        con_iva: Si es True, agrega 19% de IVA al precio
        
    Returns:
        String formateado como "$1.234.567"
    """
    if con_iva:
        precio = calcular_precio_con_iva(precio)
    return f"${int(precio):,}".replace(",", ".")


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

def mostrar_tabla_paquetes(paquetes: list, con_iva: bool = False) -> None:
    """Muestra lista de paquetes en formato tabla.
    
    Args:
        paquetes: Lista de PaqueteDTO
        con_iva: Si es True, muestra precios con IVA (19%) incluido
    """
    from src.business.paquete_service import PaqueteService
    from src.dao.politica_cancelacion_dao import PoliticaCancelacionDAO
    
    if not paquetes:
        print("No hay paquetes para mostrar.")
        return
    
    paquete_service = PaqueteService()
    
    # Obtener políticas para mostrar nombre
    politica_dao = PoliticaCancelacionDAO()
    politicas = {p.id: p.nombre for p in politica_dao.listar_todas()}
    
    # Encabezado
    precio_header = "PRECIO (IVA inc.)" if con_iva else "PRECIO"
    print("\n" + "="*140)
    print(f"{'ID':<5} {'NOMBRE':<35} {precio_header:<18} {'CUPOS':<8} {'POLITICA':<12} {'FECHA INICIO':<12} {'FECHA FIN':<12}")
    print("="*140)
    
    for p in paquetes:
        precio_mostrar = calcular_precio_con_iva(p.precio_total) if con_iva else p.precio_total
        precio = f"${int(precio_mostrar):,}".replace(",", ".")
        fecha_inicio = str(p.fecha_inicio)[:10] if p.fecha_inicio else "N/A"
        fecha_fin = str(p.fecha_fin)[:10] if p.fecha_fin else "N/A"
        nombre = (p.nombre[:32] + "...") if len(p.nombre) > 35 else p.nombre
        politica_nombre = politicas.get(p.politica_id, "N/A")
        
        print(f"{p.id:<5} {nombre:<35} {precio:<18} {p.cupos_disponibles:<8} {politica_nombre:<12} {fecha_inicio:<12} {fecha_fin:<12}")
        
        # Mostrar descripción si existe
        if p.descripcion:
            desc = p.descripcion if len(p.descripcion) <= 120 else p.descripcion[:117] + "..."
            print(f"      Descripción: {desc}")
        
        # Mostrar TODAS las actividades incluidas en el paquete
        if p.id:
            actividades = paquete_service.obtener_actividades_paquete(p.id)
            if actividades:
                print("      Actividades: ", end="")
                # Mostrar todas las actividades, no solo 3
                acts_str = ", ".join([f"{a['nombre']} ({a['duracion_horas']}h)" for a in actividades])
                print(acts_str)
        print("-"*140)
    
    if con_iva:
        print("* Precios incluyen IVA (19%)")
    print("="*140 + "\n")


def mostrar_tabla_destinos(destinos: list, con_iva: bool = False) -> None:
    """Muestra lista de destinos en formato tabla con politica de cancelacion.
    
    Args:
        destinos: Lista de DestinoDTO
        con_iva: Si es True, muestra precios con IVA (19%) incluido
    """
    if not destinos:
        print("No hay destinos para mostrar.")
        return
    
    # Obtener políticas para mostrar nombre
    from src.dao.politica_cancelacion_dao import PoliticaCancelacionDAO
    politica_dao = PoliticaCancelacionDAO()
    politicas = {p.id: p.nombre for p in politica_dao.listar_todas()}
    
    # Encabezado
    costo_header = "COSTO (IVA inc.)" if con_iva else "COSTO BASE"
    print("\n" + "="*125)
    print(f"{'ID':<5} {'NOMBRE':<25} {costo_header:<18} {'CUPOS':<8} {'POLITICA':<12} {'DESCRIPCION':<50}")
    print("="*125)
    
    for d in destinos:
        costo_mostrar = calcular_precio_con_iva(d.costo_base) if con_iva else d.costo_base
        costo = f"${int(costo_mostrar):,}".replace(",", ".")
        descripcion = (d.descripcion[:47] + "...") if len(d.descripcion) > 50 else d.descripcion
        politica_nombre = politicas.get(d.politica_id, "Flexible")
        print(f"{d.id:<5} {d.nombre:<25} {costo:<18} {d.cupos_disponibles:<8} {politica_nombre:<12} {descripcion:<50}")
    
    if con_iva:
        print("* Precios incluyen IVA (19%)")
    print("="*125 + "\n")

def mostrar_tabla_actividades(actividades: list, con_iva: bool = False) -> None:
    """Muestra lista de actividades en formato tabla.
    
    Args:
        actividades: Lista de ActividadDTO
        con_iva: Si es True, muestra precios con IVA (19%) incluido
    """
    if not actividades:
        print("No hay actividades para mostrar.")
        return
    
    # Obtener nombres de destinos
    from src.dao.destino_dao import DestinoDAO
    destino_dao = DestinoDAO()
    destinos = {d.id: d.nombre for d in destino_dao.listar_todos()}
    
    # Encabezado
    precio_header = "PRECIO (IVA)" if con_iva else "PRECIO"
    print("\n" + "="*125)
    print(f"{'ID':<5} {'NOMBRE':<30} {'DURACION':<10} {precio_header:<15} {'DESTINO':<18} {'DESCRIPCION':<40}")
    print("="*125)
    
    for a in actividades:
        duracion = f"{a.duracion_horas}h"
        precio_mostrar = calcular_precio_con_iva(a.precio_base) if con_iva else a.precio_base
        precio = f"${int(precio_mostrar):,}".replace(",", ".")
        descripcion = (a.descripcion[:37] + "...") if a.descripcion and len(a.descripcion) > 40 else (a.descripcion or "Sin descripcion")
        nombre = (a.nombre[:27] + "...") if len(a.nombre) > 30 else a.nombre
        # Mostrar nombre del destino en lugar de ID
        destino_nombre = destinos.get(a.destino_id, f"ID:{a.destino_id}")
        destino_nombre = (destino_nombre[:15] + "...") if len(destino_nombre) > 18 else destino_nombre
        
        print(f"{a.id:<5} {nombre:<30} {duracion:<10} {precio:<15} {destino_nombre:<18} {descripcion:<40}")
    
    if con_iva:
        print("* Precios incluyen IVA (19%)")
    print("="*125 + "\n")

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