from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.actividad_dto import ActividadDTO


class ActividadDAO():
    #Maneja todas las operaciones de base de datos relacionadas con Actividades.
    
    def crear(self, actividad_dto): 
        #Inserta una nueva actividad
        ...
    
    def obtener_por_id(self, id): 
        #Busca actividad por ID
        ...
    
    def actualizar(self, id, actividad_dto): 
        #Actualiza datos de la actividad
        ...
    
    def eliminar(self, id): 
        #Elimina una actividad
        ...
    
    def listar_todas(self): 
        #Retorna lista de todas las actividades
        ...
    
    def listar_por_destino(self, destino_id): 
        #Retorna actividades de un destino específico
        ...