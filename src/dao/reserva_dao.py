from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.reserva_dto import ReservaDTO


class ReservaDAO():
    #Maneja todas las operaciones de base de datos relacionadas con Reservas.
    
    def crear(self, reserva_dto): 
        #Inserta una nueva reserva en estado 'pendiente'
        ...
    def obtener_por_id(self, id): 
        #Busca reserva por ID con JOINs a cliente y paquete
        ...
    def actualizar(self, id, reserva_dto): 
        #Actualiza datos de la reserva
        ...
    def cambiar_estado(self, id, nuevo_estado): 
        #Cambia el estado de la reserva
        ...
    def listar_por_cliente(self, cliente_id): 
        #Retorna reservas de un cliente
        ...
    def listar_por_paquete(self, paquete_id): 
        #Retorna reservas de un paquete
        ...
    def listar_por_estado(self, estado): 
        #Retorna reservas filtradas por estado
        ...
    def confirmar(self, id): 
        #Cambia estado a 'confirmada'
        ...
    def marcar_como_pagada(self, id): 
        #Cambia estado a 'pagada'
        ...
    def cancelar(self, id): 
        #Cambia estado a 'cancelada' y restaura cupos
        ...