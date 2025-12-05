class ActividadDTO:
    # Clase que representa los datos de una actividad turística.
    def __init__(self, id:int | None, nombre:str, descripcion: str, duracion_horas: int, precio_base: float, destino_id:int):
        self.id=id
        self.nombre=nombre
        self.descripcion=descripcion
        self.duracion_horas=duracion_horas
        self.precio_base=precio_base
        self.destino_id=destino_id
    
    def __repr__(self):
        return (f"ActividadDTO(id={self.id}, nombre='{self.nombre}', duracion={self.duracion_horas}h, precio={self.precio_base})")