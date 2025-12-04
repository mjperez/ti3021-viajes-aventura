class DestinoDTO:
    # Clase que representa los datos de un destino turístico.
    def __init__(self, id:int | None, nombre:str, descripcion:str, costo_base:float):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.costo_base = costo_base

    def __repr__(self):
        return f"DestinoDTO(id={self.id}, nombre='{self.nombre}', costo={self.costo_base})"