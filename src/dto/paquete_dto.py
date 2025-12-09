from datetime import datetime


class PaqueteDTO:
    """Transfer Object para Paquete. Representa los datos de un paquete turístico."""
    def __init__(self, id:int | None, nombre:str, fecha_inicio: datetime, fecha_fin:datetime, precio_total:int, cupos_disponibles:int, politica_id: int, descripcion:str | None = None):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.fecha_inicio=fecha_inicio
        self.fecha_fin=fecha_fin
        self.precio_total=precio_total
        self.cupos_disponibles=cupos_disponibles
        self.politica_id=politica_id

    def __repr__(self):
        return (f"PaqueteDTO(id={self.id}, nombre='{self.nombre}',precio={self.precio_total}, cupos={self.cupos_disponibles})")