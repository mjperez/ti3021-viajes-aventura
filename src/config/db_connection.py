import os
import sys

# Detectar si estamos en modo portable (PyInstaller ejecutable)
_MODO_PORTABLE = getattr(sys, 'frozen', False)

if _MODO_PORTABLE:
    # Modo portable: usar SQLite
    import sqlite3
    from datetime import datetime, timedelta
    from pathlib import Path
    
    # La BD está junto al ejecutable
    _BASE_PATH = Path(sys.executable).parent
    _DB_PATH = _BASE_PATH / "viajes_aventura.db"
    _db_initialized = False
    
    def _crear_tablas_sqlite(conn):
        """Crea las tablas del esquema."""
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                nombre TEXT NOT NULL,
                rol TEXT NOT NULL CHECK(rol IN ('ADMIN', 'CLIENTE')) DEFAULT 'CLIENTE',
                fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Destinos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                costo_base REAL NOT NULL,
                cupos_disponibles INTEGER NOT NULL DEFAULT 50,
                activo INTEGER NOT NULL DEFAULT 1,
                politica_id INTEGER NOT NULL DEFAULT 1,
                FOREIGN KEY (politica_id) REFERENCES PoliticasCancelacion(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Actividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                duracion_horas INTEGER NOT NULL,
                precio_base REAL NOT NULL DEFAULT 0.00,
                destino_id INTEGER NOT NULL,
                FOREIGN KEY (destino_id) REFERENCES Destinos(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS PoliticasCancelacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                dias_aviso INTEGER NOT NULL,
                porcentaje_reembolso INTEGER NOT NULL
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Paquetes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                fecha_inicio DATETIME NOT NULL,
                fecha_fin DATETIME NOT NULL,
                precio_total REAL NOT NULL,
                cupos_disponibles INTEGER NOT NULL DEFAULT 20,
                politica_id INTEGER NOT NULL,
                FOREIGN KEY (politica_id) REFERENCES PoliticasCancelacion(id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Paquete_Destino (
                paquete_id INTEGER NOT NULL,
                destino_id INTEGER NOT NULL,
                orden_visita INTEGER NOT NULL,
                PRIMARY KEY (paquete_id, destino_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Paquete_Actividad (
                paquete_id INTEGER NOT NULL,
                actividad_id INTEGER NOT NULL,
                PRIMARY KEY (paquete_id, actividad_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Reservas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_reserva DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                estado TEXT NOT NULL DEFAULT 'PENDIENTE',
                monto_total REAL NOT NULL,
                numero_personas INTEGER NOT NULL,
                usuario_id INTEGER NOT NULL,
                paquete_id INTEGER,
                destino_id INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Pagos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reserva_id INTEGER NOT NULL,
                fecha_pago DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                monto REAL NOT NULL,
                metodo TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'PENDIENTE'
            )
        """)
        
        conn.commit()
    
    def _insertar_datos_iniciales(conn):
        """Inserta datos iniciales si la BD está vacía."""
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM Usuarios")
        if cursor.fetchone()[0] > 0:
            return  # Ya hay datos
        
        # Usuarios (hashes bcrypt válidos)
        # Contraseñas: Admin123, Cliente123, Maria123, Juan123, Ana123
        cursor.execute("""
            INSERT INTO Usuarios (email, password_hash, nombre, rol) VALUES
            ('admin@viajes.com', '$2b$12$ZOaOFz6nUqGlpuIQSYdcUOI4BgqK7rhjK2r0n9hj7d1yyPlbdRiUe', 'Administrador', 'ADMIN'),
            ('cliente@test.com', '$2b$12$W8Z4ulDbJ6da/A5/g6TnTOmfiZNRBxdw6hpgEhA3ePO0BIy0ttHCS', 'Cliente Test', 'CLIENTE'),
            ('maria@email.com', '$2b$12$W8Z4ulDbJ6da/A5/g6TnTOmfiZNRBxdw6hpgEhA3ePO0BIy0ttHCS', 'María González', 'CLIENTE'),
            ('juan@email.com', '$2b$12$W8Z4ulDbJ6da/A5/g6TnTOmfiZNRBxdw6hpgEhA3ePO0BIy0ttHCS', 'Juan Pérez', 'CLIENTE'),
            ('ana@email.com', '$2b$12$W8Z4ulDbJ6da/A5/g6TnTOmfiZNRBxdw6hpgEhA3ePO0BIy0ttHCS', 'Ana Rodríguez', 'CLIENTE')
        """)
        
        # Políticas
        cursor.execute("""
            INSERT INTO PoliticasCancelacion (nombre, dias_aviso, porcentaje_reembolso) VALUES
            ('Flexible', 3, 100),
            ('Estricta', 7, 50)
        """)
        
        # Destinos (CLP) - con política de cancelación
        cursor.execute("""
            INSERT INTO Destinos (nombre, descripcion, costo_base, cupos_disponibles, politica_id) VALUES
            ('Machu Picchu', 'Ciudadela inca en las montañas de los Andes', 1200000, 50, 1),
            ('Patagonia', 'Región natural de América del Sur', 1850000, 30, 2),
            ('Amazonas', 'Selva tropical más grande del mundo', 1500000, 40, 1)
        """)
        
        # Actividades (CLP)
        cursor.execute("""
            INSERT INTO Actividades (nombre, descripcion, duracion_horas, precio_base, destino_id) VALUES
            ('Trekking a la ciudadela', 'Caminata guiada por el camino inca', 8, 85000, 1),
            ('Tour por las ruinas', 'Visita guiada con historiador', 4, 45000, 1),
            ('Glaciar trekking', 'Caminata sobre hielo glaciar', 6, 120000, 2),
            ('Kayak en lagos', 'Navegación en kayak por lagos patagónicos', 5, 95000, 2),
            ('Safari fotográfico', 'Tour de observación de fauna silvestre', 10, 150000, 3),
            ('Navegación río Amazonas', 'Paseo en bote por el río', 6, 110000, 3)
        """)
        
        # Paquetes (CLP)
        hoy = datetime.now()
        cursor.execute("""
            INSERT INTO Paquetes (nombre, descripcion, fecha_inicio, fecha_fin, precio_total, cupos_disponibles, politica_id) VALUES
            (?, ?, ?, ?, 1450000, 25, 1),
            (?, ?, ?, ?, 2150000, 15, 2),
            (?, ?, ?, ?, 1890000, 20, 1)
        """, (
            'Aventura Machu Picchu Completo', 'Paquete completo: trekking + tour guiado',
            (hoy + timedelta(days=30)).strftime('%Y-%m-%d'), (hoy + timedelta(days=34)).strftime('%Y-%m-%d'),
            'Patagonia Extrema', 'Glaciar trekking + kayak en lagos patagónicos',
            (hoy + timedelta(days=45)).strftime('%Y-%m-%d'), (hoy + timedelta(days=51)).strftime('%Y-%m-%d'),
            'Expedición Amazonas Total', 'Safari fotográfico + navegación por el río',
            (hoy + timedelta(days=60)).strftime('%Y-%m-%d'), (hoy + timedelta(days=67)).strftime('%Y-%m-%d')
        ))
        
        # Relaciones
        cursor.execute("INSERT INTO Paquete_Destino VALUES (1,1,1), (2,2,1), (3,3,1)")
        cursor.execute("INSERT INTO Paquete_Actividad VALUES (1,1), (1,2), (2,3), (2,4), (3,5), (3,6)")
        
        # Reservas de prueba (diferentes estados)
        cursor.execute("""
            INSERT INTO Reservas (fecha_reserva, estado, monto_total, numero_personas, usuario_id, paquete_id, destino_id) VALUES
            (?, 'CONFIRMADA', 2900000, 2, 2, 1, NULL),
            (?, 'PENDIENTE', 1450000, 1, 3, 1, NULL),
            (?, 'PAGADA', 4300000, 2, 4, 2, NULL),
            (?, 'CONFIRMADA', 1200000, 1, 5, NULL, 1),
            (?, 'CANCELADA', 1850000, 1, 3, NULL, 2),
            (?, 'PENDIENTE', 3780000, 2, 2, 3, NULL)
        """, (
            (hoy - timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=10)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=15)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        # Pagos de prueba
        cursor.execute("""
            INSERT INTO Pagos (reserva_id, fecha_pago, monto, metodo, estado) VALUES
            (1, ?, 2900000, 'TARJETA', 'COMPLETADO'),
            (3, ?, 4300000, 'TRANSFERENCIA', 'COMPLETADO'),
            (4, ?, 1200000, 'EFECTIVO', 'COMPLETADO'),
            (6, ?, 1890000, 'TARJETA', 'PENDIENTE')
        """, (
            (hoy - timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=9)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=6)).strftime('%Y-%m-%d %H:%M:%S'),
            (hoy - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
        ))
        
        conn.commit()
    
    def _init_db_if_needed():
        """Inicializa la base de datos SQLite si no existe."""
        global _db_initialized
        if _db_initialized:
            return
        
        conn = sqlite3.connect(str(_DB_PATH))
        conn.row_factory = sqlite3.Row
        try:
            _crear_tablas_sqlite(conn)
            _insertar_datos_iniciales(conn)
            _db_initialized = True
        finally:
            conn.close()
    
    def obtener_conexion():  # type: ignore[no-redef]
        """Obtiene conexión SQLite."""
        _init_db_if_needed()
        conn = sqlite3.connect(str(_DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    
    def cerrar_conexion():  # type: ignore[no-redef]
        """No hace nada en SQLite - cada operación cierra su conexión."""
        pass
    
    def _ejecutar_query(query: str, params=None, fetch_mode='all'):  # type: ignore[no-redef]
        """Ejecuta queries en SQLite."""
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        # Convertir placeholders MySQL (%s) a SQLite (?)
        query_sqlite = query.replace('%s', '?')
        
        try:
            cursor.execute(query_sqlite, params or ())
            
            if fetch_mode == 'all':
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
            elif fetch_mode == 'one':
                row = cursor.fetchone()
                return dict(row) if row else None
            elif fetch_mode == 'none':
                conn.commit()
                return cursor.lastrowid if cursor.lastrowid > 0 else cursor.rowcount
        except sqlite3.Error as e:
            if fetch_mode == 'none':
                conn.rollback()
            print(f"Error ejecutando query: {e}")
            raise
        finally:
            conn.close()

else:
    # Modo normal: usar MySQL
    import pymysql
    from dotenv import load_dotenv

    from src.utils import DB_CHARSET, DB_PORT_DEFAULT

    _instancia_conexion = None
    load_dotenv()

    class Conexion():
        #Gestiona la conexión a la base de datos MySQL.

        def __init__(self):
            self.host = str(os.getenv("DB_HOST","localhost"))
            self.name = str(os.getenv("DB_NAME",""))
            self.user = str(os.getenv("DB_USER","root"))
            self.passwd = str(os.getenv("DB_PASSWORD",""))
            self.port = int(os.getenv("DB_PORT", str(DB_PORT_DEFAULT)))

            self.conn = None
        
        def _conectar(self):
            if not self.conn:
                try:
                    self.conn = pymysql.connect(
                        user=self.user,
                        password=self.passwd, 
                        host=self.host, 
                        database=self.name,
                        port=self.port,
                        charset=DB_CHARSET,
                        cursorclass=pymysql.cursors.DictCursor
                        )
                except pymysql.MySQLError as e:
                    print(f"Error en la conexión a la base de datos: {e}")
                    raise
            return self.conn
        
        def _cerrar(self):
            if self.conn:
                self.conn.close()
                self.conn = None

    def obtener_conexion():
        global _instancia_conexion
        if _instancia_conexion is None:
            _instancia_conexion = Conexion()
        return _instancia_conexion._conectar()
        
    def cerrar_conexion():
        global _instancia_conexion
        if _instancia_conexion:
            _instancia_conexion._cerrar()
            _instancia_conexion = None

    def _ejecutar_query(query: str, params=None, fetch_mode='all'):
        # Funcion privada para ejecutar queries.

        conn = obtener_conexion()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params or ())
            
            if fetch_mode == 'all': # SELECT y retorna muchas filas
                return cursor.fetchall()
            elif fetch_mode == 'one': # SELECT y retornar una sola fila
                return cursor.fetchone()
            elif fetch_mode == 'none': # INSERT, UPDATE, DELETE
                conn.commit()
                # Si es INSERT (lastrow>0) retorna ID, si es UPDATE/DELETE (lastrow=0) retorna filas afectadas
                return cursor.lastrowid if cursor.lastrowid > 0 else cursor.rowcount 

        except pymysql.MySQLError as e:
            if fetch_mode == 'none': # Si trato de modificar, rollback
                conn.rollback()
            print(f"Error ejecutando query: {e}")
            raise
        finally:
            cursor.close()


def ejecutar_consulta(query: str, params=None) -> list[dict] | None:
    """
    Ejecuta SELECT que retorna MÚLTIPLES filas.
    
    Args:
        query: Consulta SQL con placeholders %s
        params: Tupla de parámetros para el query
    
    Returns:
        Lista de diccionarios (cada dict es una fila) o lista vacía si no hay resultados.
        Ejemplo: [{'id': 1, 'nombre': 'París'}, {'id': 2, 'nombre': 'Roma'}]
    """
    return _ejecutar_query(query, params, fetch_mode='all') # type: ignore


def ejecutar_consulta_uno(query: str, params=None) -> dict | None:
    """
    Ejecuta SELECT que retorna UNA SOLA fila.
    
    Args:
        query: Consulta SQL con placeholders %s
        params: Tupla de parámetros para el query
    
    Returns:
        Diccionario con los campos de la fila o None si no existe.
        Ejemplo: {'id': 1, 'nombre': 'París', 'costo_base': 1200.00}
    """
    return _ejecutar_query(query, params, fetch_mode='one') # type: ignore


def ejecutar_insercion(query: str, params=None) -> int:
    """
    Ejecuta INSERT en la base de datos.
    
    Args:
        query: Consulta INSERT con placeholders %s
        params: Tupla de valores para insertar
    
    Returns:
        ID autogenerado (lastrowid) del registro insertado.
        Ejemplo: 5 (el nuevo ID del destino insertado)
    """
    return _ejecutar_query(query, params, fetch_mode='none') # type: ignore


def ejecutar_actualizacion(query: str, params=None) -> int:
    """
    Ejecuta UPDATE o DELETE en la base de datos.
    
    Args:
        query: Consulta UPDATE/DELETE con placeholders %s
        params: Tupla de valores para la operación
    
    Returns:
        Número de filas afectadas (rowcount).
        Ejemplo: 1 si actualizó/eliminó 1 fila, 0 si no encontró nada
    """
    return _ejecutar_query(query, params, fetch_mode='none') # type: ignore