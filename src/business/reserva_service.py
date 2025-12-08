"""Service Layer para Reservas

Encapsula la lógica de negocio relacionada con reservas.
Intermediario entre la UI y el DAO para mantener separación de capas.
Reemplaza completamente a reserva_manager.py (eliminando redundancia).
"""

from datetime import datetime, timedelta

from src.dao.destino_dao import DestinoDAO
from src.dao.paquete_dao import PaqueteDAO
from src.dao.reserva_dao import ReservaDAO
from src.dto.reserva_dto import ReservaDTO
from src.utils.constants import ESTADOS_RESERVA
from src.utils.exceptions import ValidacionError

# Máquina de estados: define transiciones válidas
# Formato: estado_actual -> [estados_permitidos]
TRANSICIONES_VALIDAS = {
    "PENDIENTE": ["PAGADA", "CANCELADA"],           # Cliente puede pagar o cancelar
    "PAGADA": ["CONFIRMADA", "CANCELADA"],          # Admin confirma, o se puede cancelar
    "CONFIRMADA": ["COMPLETADA", "CANCELADA"],      # Se completa el viaje o se cancela (con política)
    "COMPLETADA": [],                                # Estado final, no hay más transiciones
    "CANCELADA": []                                  # Estado final, no hay más transiciones
}


class ReservaService:
    """Servicio para gestión de reservas."""
    
    def __init__(self):
        """Inicializa el servicio con sus DAOs."""
        self.reserva_dao = ReservaDAO()
        self.paquete_dao = PaqueteDAO()
        self.destino_dao = DestinoDAO()
    
    def obtener_reserva(self, reserva_id: int) -> ReservaDTO | None:
        """Obtiene una reserva por ID.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            ReservaDTO o None si no existe
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        return self.reserva_dao.obtener_por_id(reserva_id)
    
    def listar_reservas_cliente(self, cliente_id: int) -> list[ReservaDTO]:
        """Lista todas las reservas de un cliente.
        
        Args:
            cliente_id: ID del cliente
            
        Returns:
            Lista de ReservaDTO del cliente
        """
        if cliente_id <= 0:
            raise ValidacionError("El ID del cliente debe ser mayor a 0")
        
        return self.reserva_dao.listar_por_cliente(cliente_id)
    
    def listar_reservas_paquete(self, paquete_id: int) -> list[ReservaDTO]:
        """Lista todas las reservas de un paquete.
        
        Args:
            paquete_id: ID del paquete
            
        Returns:
            Lista de ReservaDTO del paquete
        """
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        
        return self.reserva_dao.listar_por_paquete(paquete_id)
    
    def listar_reservas_destino(self, destino_id: int) -> list[ReservaDTO]:
        """Lista todas las reservas de un destino.
        
        Args:
            destino_id: ID del destino
            
        Returns:
            Lista de ReservaDTO del destino
        """
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        
        return self.reserva_dao.listar_por_destino(destino_id)
    
    def listar_todas_reservas(self) -> list[ReservaDTO]:
        """Lista todas las reservas del sistema.
        
        Returns:
            Lista de todas las ReservaDTO
        """
        return self.reserva_dao.listar_todas()
    
    def cambiar_estado_reserva(self, reserva_id: int, nuevo_estado: str) -> bool:
        """Cambia el estado de una reserva validando transiciones.
        
        Args:
            reserva_id: ID de la reserva
            nuevo_estado: Nuevo estado (PENDIENTE, PAGADA, CONFIRMADA, CANCELADA, COMPLETADA)
            
        Returns:
            True si se actualizó correctamente
            
        Raises:
            ValidacionError: Si los datos no son válidos o transición no permitida
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        estados_validos = list(TRANSICIONES_VALIDAS.keys())
        if nuevo_estado not in estados_validos:
            raise ValidacionError(f"Estado no válido. Debe ser uno de: {', '.join(estados_validos)}")
        
        # Verificar existencia
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError(f"No existe una reserva con ID {reserva_id}")
        
        # Validar transición de estado
        estado_actual = reserva.estado
        transiciones_permitidas = TRANSICIONES_VALIDAS.get(estado_actual, [])
        
        if nuevo_estado not in transiciones_permitidas:
            raise ValidacionError(
                f"Transición no permitida: {estado_actual} → {nuevo_estado}. "
                f"Transiciones válidas desde {estado_actual}: {transiciones_permitidas or 'ninguna'}"
            )
        
        # Actualizar estado usando el DAO
        if nuevo_estado == "CONFIRMADA":
            return self.reserva_dao.confirmar(reserva_id)
        elif nuevo_estado == "CANCELADA":
            return self.reserva_dao.cancelar(reserva_id)
        elif nuevo_estado == "PAGADA":
            return self.reserva_dao.marcar_como_pagada(reserva_id)
        elif nuevo_estado == "COMPLETADA":
            return self.reserva_dao.completar(reserva_id)
        else:
            raise ValidacionError(f"Cambio de estado a '{nuevo_estado}' no implementado")
      
    def crear_reserva_paquete(self, usuario_id: int, paquete_id: int, num_personas: int) -> int:
        """Crea una reserva de paquete y reduce cupos.
        
        Args:
            usuario_id: ID del usuario
            paquete_id: ID del paquete
            num_personas: Número de personas
            
        Returns:
            ID de la reserva creada
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones
        if usuario_id <= 0:
            raise ValidacionError("El ID del usuario debe ser mayor a 0")
        if paquete_id <= 0:
            raise ValidacionError("El ID del paquete debe ser mayor a 0")
        if num_personas <= 0:
            raise ValidacionError("El número de personas debe ser mayor a 0")
        
        # Validar que el paquete existe
        paquete = self.paquete_dao.obtener_por_id(paquete_id)
        if not paquete:
            raise ValidacionError("El paquete no existe")
        
        # Verificar disponibilidad
        if paquete.cupos_disponibles < num_personas:
            raise ValidacionError("No hay cupos suficientes disponibles")
        
        # Calcular precio total
        precio_total = paquete.precio_total * num_personas
        
        # Crear DTO de reserva
        reserva = ReservaDTO(
            id=None,
            fecha_reserva=datetime.now(),
            estado=ESTADOS_RESERVA[0],  # "PENDIENTE"
            monto_total=precio_total,
            numero_personas=num_personas,
            usuario_id=usuario_id,
            paquete_id=paquete_id,
            destino_id=None
        )
        
        try:
            # Crear reserva
            reserva_id = self.reserva_dao.crear(reserva)
            
            # Reducir cupos del paquete
            cupos_reducidos = 0
            for i in range(num_personas): # type: ignore
                if not self.paquete_dao.reducir_cupo(paquete_id):
                    # Rollback: devolver cupos ya reducidos
                    for _ in range(cupos_reducidos):
                        self.paquete_dao.aumentar_cupo(paquete_id)
                    raise ValidacionError("Error al reducir cupos del paquete")
                cupos_reducidos += 1
            
            return reserva_id
        except Exception as e:
            raise ValidacionError(f"Error al crear reserva: {str(e)}")
    
    def crear_reserva_destino(self, usuario_id: int, destino_id: int, num_personas: int) -> int:
        """Crea una reserva de destino individual y reduce cupos.
        
        Args:
            usuario_id: ID del usuario
            destino_id: ID del destino
            num_personas: Número de personas
            
        Returns:
            ID de la reserva creada
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        # Validaciones
        if usuario_id <= 0:
            raise ValidacionError("El ID del usuario debe ser mayor a 0")
        if destino_id <= 0:
            raise ValidacionError("El ID del destino debe ser mayor a 0")
        if num_personas <= 0:
            raise ValidacionError("El número de personas debe ser mayor a 0")
        
        # Validar que el destino existe
        destino = self.destino_dao.obtener_por_id(destino_id)
        if not destino:
            raise ValidacionError("El destino no existe")
        
        # Verificar disponibilidad
        if destino.cupos_disponibles < num_personas:
            raise ValidacionError("No hay cupos suficientes disponibles en este destino")
        
        # Calcular precio total
        precio_total = destino.costo_base * num_personas
        
        # Crear DTO de reserva
        reserva = ReservaDTO(
            id=None,
            fecha_reserva=datetime.now(),
            estado=ESTADOS_RESERVA[0],  # "PENDIENTE"
            monto_total=precio_total,
            numero_personas=num_personas,
            usuario_id=usuario_id,
            paquete_id=None,
            destino_id=destino_id
        )
        
        try:
            # Crear reserva
            reserva_id = self.reserva_dao.crear(reserva)
            
            # Reducir cupos del destino
            cupos_reducidos = 0
            for i in range(num_personas): # type: ignore
                if not self.destino_dao.reducir_cupo(destino_id):
                    # Rollback: devolver cupos ya reducidos
                    for _ in range(cupos_reducidos):
                        self.destino_dao.aumentar_cupo(destino_id)
                    raise ValidacionError("Error al reducir cupos del destino")
                cupos_reducidos += 1
            
            return reserva_id
        except Exception as e:
            raise ValidacionError(f"Error al crear reserva de destino: {str(e)}")
    
    def cancelar_reserva(self, reserva_id: int) -> dict:
        """Cancela una reserva aplicando política de cancelación.
        
        Verifica la política de cancelación del paquete o destino y calcula reembolso
        según días de aviso y porcentaje establecido. Las reservas CONFIRMADAS pueden
        cancelarse pero se aplica la política de reembolso.
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            Diccionario con información del reembolso:
            - cancelada: bool
            - monto_total: float
            - porcentaje_reembolso: float
            - monto_reembolso: float
            - mensaje: str
            
        Raises:
            ValidacionError: Si los datos no son válidos o transición no permitida
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        # Obtener la reserva
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError("La reserva no existe")
        
        # Validar transición de estado usando máquina de estados
        estado_actual = reserva.estado
        if "CANCELADA" not in TRANSICIONES_VALIDAS.get(estado_actual, []):
            raise ValidacionError(
                f"No se puede cancelar una reserva en estado '{estado_actual}'. "
                f"Solo se pueden cancelar reservas en estado: PENDIENTE, PAGADA o CONFIRMADA."
            )
        
        from src.config.db_connection import ejecutar_consulta_uno
        politica = None
        fecha_referencia = None
        
        # Verificar política de cancelación para paquetes
        if reserva.paquete_id:
            paquete = self.paquete_dao.obtener_por_id(reserva.paquete_id)
            if paquete and paquete.fecha_inicio:
                fecha_referencia = datetime.strptime(str(paquete.fecha_inicio)[:10], '%Y-%m-%d')
                
                politica_sql = """
                    SELECT pc.nombre, pc.dias_aviso, pc.porcentaje_reembolso
                    FROM PoliticasCancelacion pc
                    JOIN Paquetes p ON p.politica_id = pc.id
                    WHERE p.id = %s
                """
                politica = ejecutar_consulta_uno(politica_sql, (reserva.paquete_id,))
        
        # Verificar política de cancelación para destinos
        elif reserva.destino_id:
            destino = self.destino_dao.obtener_por_id(reserva.destino_id)
            if destino:
                fecha_referencia = reserva.fecha_reserva + timedelta(days=30) if isinstance(reserva.fecha_reserva, datetime) else datetime.strptime(str(reserva.fecha_reserva)[:10], '%Y-%m-%d') + timedelta(days=30)
                
                politica_sql = """
                    SELECT pc.nombre, pc.dias_aviso, pc.porcentaje_reembolso
                    FROM PoliticasCancelacion pc
                    JOIN Destinos d ON d.politica_id = pc.id
                    WHERE d.id = %s
                """
                politica = ejecutar_consulta_uno(politica_sql, (reserva.destino_id,))
        
        # Calcular reembolso según política
        porcentaje_reembolso = 100  # Por defecto, reembolso completo
        monto_reembolso = float(reserva.monto_total)
        mensaje = "Reembolso completo (100%)"
        
        if politica and fecha_referencia:
            hoy = datetime.now()
            dias_hasta_fecha = (fecha_referencia - hoy).days
            dias_minimos = politica['dias_aviso']
            
            # Si no cumple días mínimos de aviso
            if dias_hasta_fecha < dias_minimos:
                # Para reservas PENDIENTES, no permitir cancelar
                if estado_actual == "PENDIENTE":
                    tipo_reserva = "paquete" if reserva.paquete_id else "destino"
                    raise ValidacionError(
                        f"No se puede cancelar. Política '{politica['nombre']}' requiere "
                        f"{dias_minimos} días de aviso. Quedan {dias_hasta_fecha} días para el {tipo_reserva}."
                    )
                # Para PAGADA o CONFIRMADA, aplicar porcentaje reducido (o 0%)
                porcentaje_reembolso = 0.0
                monto_reembolso = 0.0
                mensaje = f"Sin reembolso - Cancelación tardía (menos de {dias_minimos} días de aviso)"
            else:
                # Cumple con días de aviso, aplicar porcentaje de la política
                porcentaje_reembolso = int(politica['porcentaje_reembolso'])
                monto_reembolso = float(reserva.monto_total) * (porcentaje_reembolso / 100)
                
                if porcentaje_reembolso == 100:
                    mensaje = f"Reembolso completo (100%) - Política '{politica['nombre']}'"
                elif porcentaje_reembolso > 0:
                    mensaje = f"Reembolso parcial ({porcentaje_reembolso}%) - Política '{politica['nombre']}'"
                else:
                    mensaje = f"Sin reembolso - Política '{politica['nombre']}'"
        
        # Mostrar información de reembolso al cliente
        print(f"\n{'='*50}")
        print("INFORMACIÓN DE CANCELACIÓN")
        print(f"{'='*50}")
        print(f"Estado actual de la reserva: {estado_actual}")
        print(f"Monto total pagado: ${int(reserva.monto_total):,}".replace(",", "."))
        print(f"Porcentaje de reembolso: {int(porcentaje_reembolso)}%")
        print(f"Monto a reembolsar: ${int(monto_reembolso):,}".replace(",", "."))
        print(f"Detalle: {mensaje}")
        print(f"{'='*50}\n")
        
        # Cancelar la reserva
        if not self.reserva_dao.cancelar(reserva_id):
            return {
                "cancelada": False,
                "monto_total": int(reserva.monto_total),
                "porcentaje_reembolso": 0,
                "monto_reembolso": 0,
                "mensaje": "Error al cancelar la reserva"
            }
        
        # Devolver los cupos según el tipo de reserva
        if reserva.paquete_id:
            for _ in range(reserva.numero_personas):
                self.paquete_dao.aumentar_cupo(reserva.paquete_id)
        elif reserva.destino_id:
            for _ in range(reserva.numero_personas):
                self.destino_dao.aumentar_cupo(reserva.destino_id)
        
        return {
            "cancelada": True,
            "monto_total": int(reserva.monto_total),
            "porcentaje_reembolso": int(porcentaje_reembolso),
            "monto_reembolso": int(monto_reembolso),
            "mensaje": mensaje
        }
    
    def confirmar_reserva(self, reserva_id: int) -> bool:
        """Confirma una reserva pagada (admin aprueba después del pago).
        
        Flujo: PENDIENTE -> (cliente paga) -> PAGADA -> (admin confirma) -> CONFIRMADA
        
        Args:
            reserva_id: ID de la reserva
            
        Returns:
            True si se confirmó correctamente
            
        Raises:
            ValidacionError: Si los datos no son válidos
        """
        if reserva_id <= 0:
            raise ValidacionError("El ID de la reserva debe ser mayor a 0")
        
        # Verificar que la reserva existe
        reserva = self.reserva_dao.obtener_por_id(reserva_id)
        if not reserva:
            raise ValidacionError("La reserva no existe")
        
        # Verificar que está en estado PAGADA (el cliente ya pagó)
        if reserva.estado != "PAGADA":
            raise ValidacionError(f"La reserva debe estar en estado PAGADA para confirmar. Estado actual: {reserva.estado}")
        
        # Confirmar la reserva
        return self.reserva_dao.confirmar(reserva_id)
