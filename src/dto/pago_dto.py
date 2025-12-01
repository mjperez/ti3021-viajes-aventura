from datetime import datetime


class PagoDTO:
    # Clase que representa los datos de un pago.
    def __init__(self, id:int, monto:float, fecha_pago:datetime, metodo:str, reserva_id:int, estado:str):
        self.id=id
        self.monto=monto
        self.fecha_pago=fecha_pago
        self.metodo=metodo
        self.reserva_id=reserva_id
        self.estado=estado
    
    def __repr__(self):
        return (f"PagoDTO(id={self.id}, monto={self.monto}, metodo='{self.metodo}', estado='{self.estado}')")