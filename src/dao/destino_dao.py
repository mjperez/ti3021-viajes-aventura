from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.destino_dto import DestinoDTO


class DestinoDAO():
    # Maneja todas las operaciones de base de datos relacionadas con Destinos.

    def crear(self, destino_dto): 
        #Inserta un nuevo destino
        ...
    def obtener_por_id(self, id): 
        #Busca destino por ID
        ...
    def actualizar(self, id, destino_dto): 
        #Actualiza datos del destino
        ...
    def eliminar(self, id): 
        #Elimina un destino
        ...
    def listar_todos(self): 
        #Retorna lista de todos los destinos
        ...
    def buscar_por_nombre(self,nombre): 
        #Busca destinos por nombre (LIKE)
        ...