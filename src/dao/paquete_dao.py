from src.config.db_connection import (
    ejecutar_actualizacion,
    ejecutar_consulta,
    ejecutar_consulta_uno,
    ejecutar_insercion,
)
from src.dto.paquete_dto import PaqueteDTO


class PaqueteDAO():
    #Maneja todas las operaciones de base de datos relacionadas con Paquetes.
    
    def crear(self, paquete_dto: PaqueteDTO) -> int: 
        #Inserta un nuevo paquete
        sql = "INSERT INTO Paquetes (nombre, descripcion, fecha_inicio, fecha_fin, precio_total, cupos_disponibles, politica_id) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        params = (paquete_dto.nombre, paquete_dto.descripcion, paquete_dto.fecha_inicio, paquete_dto.fecha_fin, paquete_dto.precio_total, paquete_dto.cupos_disponibles, paquete_dto.politica_id)
        return ejecutar_insercion(sql, params)
    
    def obtener_por_id(self, id: int) -> PaqueteDTO | None: 
        #Busca paquete por ID con JOIN a destinos y política
        sql = "SELECT * FROM Paquetes WHERE id=%s"
        params = (id,)
        paquete = ejecutar_consulta_uno(sql, params)
        
        if not paquete:
            return None
        
        return PaqueteDTO(
            id=paquete['id'],
            nombre=paquete['nombre'],
            fecha_inicio=paquete['fecha_inicio'],
            fecha_fin=paquete['fecha_fin'],
            precio_total=paquete['precio_total'],
            cupos_disponibles=paquete['cupos_disponibles'],
            politica_id=paquete['politica_id'],
            descripcion=paquete.get('descripcion') or ''
        )
    
    def actualizar(self, id: int, paquete_dto: PaqueteDTO) -> bool: 
        #Actualiza datos del paquete
        sql = "UPDATE Paquetes SET nombre=%s, descripcion=%s, fecha_inicio=%s, fecha_fin=%s, precio_total=%s, cupos_disponibles=%s, politica_id=%s WHERE id=%s"
        params = (paquete_dto.nombre, paquete_dto.descripcion, paquete_dto.fecha_inicio, paquete_dto.fecha_fin, paquete_dto.precio_total, paquete_dto.cupos_disponibles, paquete_dto.politica_id, id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def eliminar(self, id: int) -> bool: 
        """Soft delete: desactiva el paquete en lugar de eliminarlo."""
        sql = "UPDATE Paquetes SET activo = FALSE WHERE id=%s"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def reactivar(self, id: int) -> bool:
        """Reactiva un paquete desactivado."""
        sql = "UPDATE Paquetes SET activo = TRUE WHERE id=%s"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def listar_todos(self) -> list[PaqueteDTO]: 
        """Retorna lista de todos los paquetes activos (para clientes)."""
        sql = "SELECT * FROM Paquetes WHERE activo = 1 ORDER BY id ASC"
        paquetes = ejecutar_consulta(sql)
        
        if not paquetes:
            return []
        
        return [
            PaqueteDTO(
                id=p['id'],
                nombre=p['nombre'],
                fecha_inicio=p['fecha_inicio'],
                fecha_fin=p['fecha_fin'],
                precio_total=p['precio_total'],
                cupos_disponibles=p['cupos_disponibles'],
                politica_id=p['politica_id'],
                descripcion=p.get('descripcion') or ''
            )
            for p in paquetes
        ]
    
    def listar_todos_admin(self) -> list[dict]: 
        """Retorna TODOS los paquetes incluyendo inactivos (para admin)."""
        sql = "SELECT * FROM Paquetes ORDER BY activo DESC, id ASC"
        paquetes = ejecutar_consulta(sql)
        
        if not paquetes:
            return []
        
        return [
            {
                'id': p['id'],
                'nombre': p['nombre'],
                'fecha_inicio': p['fecha_inicio'],
                'fecha_fin': p['fecha_fin'],
                'precio_total': p['precio_total'],
                'cupos_disponibles': p['cupos_disponibles'],
                'politica_id': p['politica_id'],
                'descripcion': p.get('descripcion') or '',
                'activo': p['activo']
            }
            for p in paquetes
        ]
    
    def listar_disponibles(self) -> list[PaqueteDTO]: 
        """Retorna paquetes activos con cupos > 0"""
        sql = "SELECT * FROM Paquetes WHERE cupos_disponibles > 0 AND activo = 1 ORDER BY id ASC"
        paquetes = ejecutar_consulta(sql)
        
        if not paquetes:
            return []
        
        return [
            PaqueteDTO(
                id=p['id'],
                nombre=p['nombre'],
                fecha_inicio=p['fecha_inicio'],
                fecha_fin=p['fecha_fin'],
                precio_total=p['precio_total'],
                cupos_disponibles=p['cupos_disponibles'],
                politica_id=p['politica_id'],
                descripcion=p.get('descripcion') or ''
            )
            for p in paquetes
        ]
    
    def reducir_cupo(self, id: int) -> bool:
        #Decrementa cupos_disponibles
        sql = "UPDATE Paquetes SET cupos_disponibles = cupos_disponibles - 1 WHERE id=%s AND cupos_disponibles > 0"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def aumentar_cupo(self, id: int) -> bool: 
        #Incrementa cupos_disponibles
        sql = "UPDATE Paquetes SET cupos_disponibles = cupos_disponibles + 1 WHERE id=%s"
        params = (id,)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def agregar_destino(self, paquete_id: int, destino_id: int) -> bool: 
        #Asocia destino al paquete
        sql = "INSERT INTO Paquete_Destino (paquete_id, destino_id, orden_visita) VALUES (%s,%s,1)"
        params = (paquete_id, destino_id)
        try:
            ejecutar_insercion(sql, params)
            return True
        except Exception:
            return False
    
    def eliminar_destino(self, paquete_id: int, destino_id: int) -> bool: 
        #Desasocia destino del paquete
        sql = "DELETE FROM Paquete_Destino WHERE paquete_id=%s AND destino_id=%s"
        params = (paquete_id, destino_id)
        filas = ejecutar_actualizacion(sql, params)
        return filas > 0
    
    def obtener_actividades_paquete(self, paquete_id: int) -> list:
        """Obtiene todas las actividades de los destinos incluidos en el paquete."""
        sql = """
        SELECT DISTINCT a.id, a.nombre, a.descripcion, a.duracion_horas, a.precio_base, d.nombre as destino_nombre
        FROM Actividades a
        JOIN Destinos d ON a.destino_id = d.id
        JOIN Paquete_Destino pd ON d.id = pd.destino_id
        WHERE pd.paquete_id = %s
        ORDER BY d.nombre, a.nombre
        """
        params = (paquete_id,)
        return ejecutar_consulta(sql, params)