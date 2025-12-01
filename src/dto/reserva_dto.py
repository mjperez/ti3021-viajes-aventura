from datetime import datetime


class ReservaDTO:
    # Clase que representa los datos de una reserva.
    def __init__(self, id:int, fecha_reserva:datetime, estado: str, monto_total: float, numero_personas: int, usuario_id: int, paquete_id: int):
        self.id=id
        self.fecha_reserva=fecha_reserva
        self.estado=estado
        self.monto_total=monto_total
        self.numero_personas=numero_personas
        self.usuario_id=usuario_id
        self.paquete_id=paquete_id
    def __repr__(self):
        return (f"ReservaDTO(id={self.id}, estado='{self.estado}', monto={self.monto_total}, personas={self.numero_personas})")