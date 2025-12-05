from datetime import datetime

from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.pago_dto import PagoDTO
from src.utils.constants import ESTADOS_PAGO


class PagoDAO():
    """Maneja todas las operaciones de base de datos relacionadas con Pagos."""
    
    def crear(self, pago_dto: PagoDTO) -> int:
        """Inserta un nuevo pago."""
        sql = """
            INSERT INTO Pagos (reserva_id, monto, metodo, estado, fecha_pago)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            pago_dto.reserva_id,
            pago_dto.monto,
            pago_dto.metodo,
            pago_dto.estado,
            pago_dto.fecha_pago
        )
        return ejecutar_insercion(sql, params)  # type: ignore
    
    def obtener_por_id(self, id: int) -> PagoDTO | None:
        """Busca pago por ID."""
        sql = "SELECT * FROM Pagos WHERE id = %s"
        result = ejecutar_consulta_uno(sql, (id,))  # type: ignore
        
        if not result:
            return None
        
        return PagoDTO(
            id=result['id'],
            reserva_id=result['reserva_id'],
            monto=result['monto'],
            metodo=result['metodo'],
            estado=result['estado'],
            fecha_pago=result['fecha_pago']
        )
    
    def obtener_por_reserva(self, reserva_id: int) -> list[PagoDTO]:
        """Retorna pagos de una reserva."""
        sql = "SELECT * FROM Pagos WHERE reserva_id = %s ORDER BY fecha_pago DESC"
        results = ejecutar_consulta(sql, (reserva_id,))  # type: ignore
        
        if not results:
            return []
        
        return [
            PagoDTO(
                id=row['id'],
                reserva_id=row['reserva_id'],
                monto=row['monto'],
                metodo=row['metodo'],
                estado=row['estado'],
                fecha_pago=row['fecha_pago']
            )
            for row in results
        ]
    
    def actualizar_estado(self, id: int, nuevo_estado: str) -> bool:
        """Cambia el estado del pago."""
        sql = "UPDATE Pagos SET estado = %s WHERE id = %s"
        filas = ejecutar_actualizacion(sql, (nuevo_estado, id))  # type: ignore
        return filas > 0
    
    def registrar_pago_completado(self, reserva_id: int, monto: float, metodo: str) -> int:
        """Procesa un pago exitoso."""
        pago = PagoDTO(
            id=None,  # Se genera automáticamente
            reserva_id=reserva_id,
            monto=monto,
            metodo=metodo,
            estado=ESTADOS_PAGO[1],  # "Completado"
            fecha_pago=datetime.now()
        )
        return self.crear(pago)
    
    def listar_por_fecha(self, fecha_inicio: str, fecha_fin: str) -> list[PagoDTO]:
        """Retorna pagos en rango de fechas."""
        sql = """
            SELECT * FROM Pagos 
            WHERE fecha_pago BETWEEN %s AND %s
            ORDER BY fecha_pago DESC
        """
        results = ejecutar_consulta(sql, (fecha_inicio, fecha_fin))  # type: ignore
        
        if not results:
            return []
        
        return [
            PagoDTO(
                id=row['id'],
                reserva_id=row['reserva_id'],
                monto=row['monto'],
                metodo=row['metodo'],
                estado=row['estado'],
                fecha_pago=row['fecha_pago']
            )
            for row in results
        ]
    
    def obtener_total_por_periodo(self, fecha_inicio: str, fecha_fin: str) -> float:
        """Suma montos de pagos completados."""
        sql = """
            SELECT SUM(monto) as total 
            FROM Pagos 
            WHERE estado = %s 
            AND fecha_pago BETWEEN %s AND %s
        """
        result = ejecutar_consulta_uno(sql, (ESTADOS_PAGO[1], fecha_inicio, fecha_fin))  # type: ignore
        
        if not result or result['total'] is None:
            return 0.0
        
        return float(result['total'])