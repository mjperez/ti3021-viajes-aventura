class DestinoDTO:
    # Clase que representa los datos de un destino turístico.
    def __init__(self, id:int | None, nombre:str, descripcion:str, costo_base:float, cupos_disponibles:int = 50, politica_id:int = 1):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.costo_base = costo_base
        self.cupos_disponibles = cupos_disponibles
        self.politica_id = politica_id  # Política de cancelación aplicable

    def __repr__(self):
        return f"DestinoDTO(id={self.id}, nombre='{self.nombre}', costo={self.costo_base}, cupos={self.cupos_disponibles}, politica_id={self.politica_id})"