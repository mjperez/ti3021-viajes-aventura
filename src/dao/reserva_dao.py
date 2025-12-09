from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.reserva_dto import ReservaDTO


class ReservaDAO():
    #Maneja todas las operaciones de base de datos relacionadas con Reservas.
    
    def crear(self, reserva_dto: ReservaDTO) -> int: 
        #Inserta una nueva reserva en estado 'pendiente'
        sql = "INSERT INTO Reservas (fecha_reserva, estado, monto_total, numero_personas, usuario_id, paquete_id, destino_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        params = (reserva_dto.fecha_reserva, reserva_dto.estado, reserva_dto.monto_total, reserva_dto.numero_personas, reserva_dto.usuario_id, reserva_dto.paquete_id, reserva_dto.destino_id)
        return ejecutar_insercion(sql, params)
    
    def obtener_por_id(self, id: int) -> ReservaDTO | None: 
        #Busca reserva por ID con JOINs a cliente y paquete
        sql = "SELECT * FROM Reservas WHERE id=%s"
        params = (id,)
        reserva = ejecutar_consulta_uno(sql, params)
        
        if not reserva:
            return None
        
        return ReservaDTO(
            id=reserva['id'],
            fecha_reserva=reserva['fecha_reserva'],
            estado=reserva['estado'],
            monto_total=reserva['monto_total'],
            numero_personas=reserva['numero_personas'],
            usuario_id=reserva['usuario_id'],
            paquete_id=reserva.get('paquete_id'),
            destino_id=reserva.get('destino_id')
        )
    
    def actualizar(self, id: int, reserva_dto: ReservaDTO) -> bool: 
        #Actualiza datos de la reserva
        sql = "UPDATE Reservas SET fecha_reserva=%s, estado=%s, monto_total=%s, numero_personas=%s, usuario_id=%s, paquete_id=%s, destino_id=%s WHERE id=%s"
        params = (reserva_dto.fecha_reserva, reserva_dto.estado, reserva_dto.monto_total, reserva_dto.numero_personas, reserva_dto.usuario_id, reserva_dto.paquete_id, reserva_dto.destino_id, id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def cambiar_estado(self, id: int, nuevo_estado: str) -> bool: 
        #Cambia el estado de la reserva
        sql = "UPDATE Reservas SET estado=%s WHERE id=%s"
        params = (nuevo_estado, id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def listar_por_cliente(self, cliente_id: int) -> list[ReservaDTO]: 
        #Retorna reservas de un cliente
        sql = "SELECT * FROM Reservas WHERE usuario_id=%s ORDER BY id ASC"
        params = (cliente_id,)
        reservas = ejecutar_consulta(sql, params)
        
        if not reservas:
            return []
        
        return [
            ReservaDTO(
                id=r['id'],
                fecha_reserva=r['fecha_reserva'],
                estado=r['estado'],
                monto_total=r['monto_total'],
                numero_personas=r['numero_personas'],
                usuario_id=r['usuario_id'],
                paquete_id=r.get('paquete_id'),
                destino_id=r.get('destino_id')
            )
            for r in reservas
        ]
    
    def listar_por_paquete(self, paquete_id: int) -> list[ReservaDTO]: 
        #Retorna reservas de un paquete
        sql = "SELECT * FROM Reservas WHERE paquete_id=%s"
        params = (paquete_id,)
        reservas = ejecutar_consulta(sql, params)
        
        if not reservas:
            return []
        
        return [
            ReservaDTO(
                id=r['id'],
                fecha_reserva=r['fecha_reserva'],
                estado=r['estado'],
                monto_total=r['monto_total'],
                numero_personas=r['numero_personas'],
                usuario_id=r['usuario_id'],
                paquete_id=r.get('paquete_id'),
                destino_id=r.get('destino_id')
            )
            for r in reservas
        ]
    
    def listar_por_estado(self, estado: str) -> list[ReservaDTO]: 
        #Retorna reservas filtradas por estado
        sql = "SELECT * FROM Reservas WHERE estado=%s ORDER BY id ASC"
        params = (estado,)
        reservas = ejecutar_consulta(sql, params)
        
        if not reservas:
            return []
        
        return [
            ReservaDTO(
                id=r['id'],
                fecha_reserva=r['fecha_reserva'],
                estado=r['estado'],
                monto_total=r['monto_total'],
                numero_personas=r['numero_personas'],
                usuario_id=r['usuario_id'],
                paquete_id=r.get('paquete_id'),
                destino_id=r.get('destino_id')
            )
            for r in reservas
        ]
    
    def confirmar(self, id: int) -> bool: 
        #Cambia estado a 'confirmada'
        return self.cambiar_estado(id, 'CONFIRMADA')
    
    def marcar_como_pagada(self, id: int) -> bool: 
        #Cambia estado a 'pagada'
        return self.cambiar_estado(id, 'PAGADA')
    
    def cancelar(self, id: int) -> bool: 
        #Cambia estado a 'cancelada' y restaura cupos
        return self.cambiar_estado(id, 'CANCELADA')
    
    def completar(self, id: int) -> bool: 
        #Cambia estado a 'completada' (viaje finalizado)
        return self.cambiar_estado(id, 'COMPLETADA')
    
    def listar_por_destino(self, destino_id: int) -> list[ReservaDTO]: 
        #Retorna reservas de un destino
        sql = "SELECT * FROM Reservas WHERE destino_id=%s"
        params = (destino_id,)
        reservas = ejecutar_consulta(sql, params)
        
        if not reservas:
            return []
        
        return [
            ReservaDTO(
                id=r['id'],
                fecha_reserva=r['fecha_reserva'],
                estado=r['estado'],
                monto_total=r['monto_total'],
                numero_personas=r['numero_personas'],
                usuario_id=r['usuario_id'],
                paquete_id=r.get('paquete_id'),
                destino_id=r.get('destino_id')
            )
            for r in reservas
        ]
    
    def listar_todas(self) -> list[ReservaDTO]:
        """Retorna todas las reservas del sistema."""
        sql = "SELECT * FROM Reservas ORDER BY id ASC"
        reservas = ejecutar_consulta(sql)
        
        if not reservas:
            return []
        
        return [
            ReservaDTO(
                id=r['id'],
                fecha_reserva=r['fecha_reserva'],
                estado=r['estado'],
                monto_total=r['monto_total'],
                numero_personas=r['numero_personas'],
                usuario_id=r['usuario_id'],
                paquete_id=r.get('paquete_id'),
                destino_id=r.get('destino_id')
            )
            for r in reservas
        ]