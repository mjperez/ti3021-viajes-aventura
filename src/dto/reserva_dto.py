from datetime import datetime


class ReservaDTO:
    # Clase que representa los datos de una reserva.
    # Montos en pesos chilenos (enteros, sin decimales)
    def __init__(self, id:int | None, fecha_reserva:datetime, estado: str, monto_total: int, numero_personas: int, usuario_id: int, paquete_id: int | None = None, destino_id: int | None = None):
        self.id=id
        self.fecha_reserva=fecha_reserva
        self.estado=estado
        self.monto_total=monto_total
        self.numero_personas=numero_personas
        self.usuario_id=usuario_id
        self.paquete_id=paquete_id
        self.destino_id=destino_id
        
        # Validar que sea paquete O destino, no ambos ni ninguno
        if (paquete_id is None and destino_id is None) or (paquete_id is not None and destino_id is not None):
            raise ValueError("Debe especificar paquete_id O destino_id, no ambos ni ninguno")
    
    def __repr__(self):
        tipo = f"paquete={self.paquete_id}" if self.paquete_id else f"destino={self.destino_id}"
        return (f"ReservaDTO(id={self.id}, {tipo}, estado='{self.estado}', monto={self.monto_total}, personas={self.numero_personas})")