from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.paquete_dto import PaqueteDTO


class PaqueteDAO():
    #Maneja todas las operaciones de base de datos relacionadas con Paquetes.
    
    def crear(self, paquete_dto): 
        #Inserta un nuevo paquete
        ...
    
    def obtener_por_id(self, id): 
        #Busca paquete por ID con JOIN a destinos y política
        ...
    
    def actualizar(self, id, paquete_dto): 
        #Actualiza datos del paquete
        ...
    
    def eliminar(self, id): 
        #Elimina un paquete
        ...
    
    def listar_todos(self): 
        #Retorna lista de todos los paquetes
        ...
    
    def listar_disponibles(self): 
        #Retorna paquetes con cupos > 0
        ...
    
    def reducir_cupo(self, id): 
        #Decrementa cupos_disponibles
        ...
    
    def aumentar_cupo(self, id): 
        #Incrementa cupos_disponibles
        ...
    
    def agregar_destino(self, paquete_id, destino_id): 
        #Asocia destino al paquete
        ...
    
    def eliminar_destino(self, paquete_id, destino_id): 
        #Desasocia destino del paquete
        ...