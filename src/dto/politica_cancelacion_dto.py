class PoliticaCancelacionDTO:
    """Transfer Object para Política de Cancelación. Representa las reglas de reembolso."""
    def __init__(self,id:int, nombre:str, dias_aviso:int, porcentaje_reembolso:int):
        self.id=id
        self.nombre=nombre
        self.dias_aviso=dias_aviso
        self.porcentaje_reembolso=porcentaje_reembolso

    def __repr__(self):
        # Representación string para debugging.
        return f"PoliticaCancelacionDTO(id='{self.id}', nombre='{self.nombre}', dias_aviso='{self.dias_aviso}', porcentaje_reembolso='{self.porcentaje_reembolso}')"