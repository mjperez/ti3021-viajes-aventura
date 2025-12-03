from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.pago_dto import PagoDTO


class PagoDAO():
    #Maneja todas las operaciones de base de datos relacionadas con Pagos.
    
    def crear(self, pago_dto): 
        #Inserta un nuevo pago
        ...
    
    def obtener_por_id(self, id): 
        #Busca pago por ID
        ...
    
    def obtener_por_reserva(self, reserva_id): 
        #Retorna pagos de una reserva
        ...
    
    def actualizar_estado(self, id, nuevo_estado): 
        #Cambia el estado del pago
        ...
    
    def registrar_pago_completado(self, reserva_id, monto, metodo): 
        #Procesa un pago exitoso
        ...
    
    def listar_por_fecha(self, fecha_inicio, fecha_fin): 
        #Retorna pagos en rango de fechas
        ...
    
    def obtener_total_por_periodo(self, fecha_inicio, fecha_fin): 
        #Suma montos de pagos completados
        ...