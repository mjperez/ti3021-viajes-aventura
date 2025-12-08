from abc import ABC, abstractmethod

class PoliticaCancelacion(ABC):
    """Clase abstracta base para las políticas de cancelación."""
    
    def __init__(self, nombre: str, dias_aviso: int, porcentaje_reembolso: int):
        self.nombre = nombre
        self.dias_aviso = dias_aviso
        self.porcentaje_reembolso = porcentaje_reembolso

    @abstractmethod
    def calcular_monto_reembolso(self, monto_total: int, dias_faltantes: int) -> int:
        """Calcula el monto a reembolsar según la lógica de la política."""
        pass

    def obtener_mensaje(self, dias_faltantes: int) -> str:
        """Retorna un mensaje explicativo."""
        pass


class PoliticaFlexible(PoliticaCancelacion):
    """Política Flexible: Permite cancelar con poco aviso y devuelve el 100%."""
    
    def calcular_monto_reembolso(self, monto_total: int, dias_faltantes: int) -> int:
        # Si cumple con los días de aviso, devuelve el porcentaje configurado (generalmente 100%)
        if dias_faltantes >= self.dias_aviso:
            return int(monto_total * (self.porcentaje_reembolso / 100))
        return 0

    def obtener_mensaje(self, dias_faltantes: int) -> str:
        if dias_faltantes >= self.dias_aviso:
            return f"Reembolso del {self.porcentaje_reembolso}% por cancelar con {dias_faltantes} días de anticipación."
        return f"Sin reembolso. Se requiere cancelar con {self.dias_aviso} días de anticipación (tienes {dias_faltantes})."


class PoliticaEstricta(PoliticaCancelacion):
    """Política Estricta: Requiere más aviso y devuelve un porcentaje menor."""
    
    def calcular_monto_reembolso(self, monto_total: int, dias_faltantes: int) -> int:
        # Si cumple con los días de aviso, devuelve el porcentaje configurado
        if dias_faltantes >= self.dias_aviso:
            return int(monto_total * (self.porcentaje_reembolso / 100))
        # Podríamos agregar lógica adicional aquí si fuera necesario
        return 0

    def obtener_mensaje(self, dias_faltantes: int) -> str:
        if dias_faltantes >= self.dias_aviso:
            return f"Reembolso parcial del {self.porcentaje_reembolso}% (Política Estricta)."
        return f"Sin reembolso. La política estricta requiere {self.dias_aviso} días de anticipación."
