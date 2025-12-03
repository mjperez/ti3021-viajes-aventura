import os

import pymysql
from dotenv import load_dotenv

_instancia_conexion = None

load_dotenv()
class Conexion():
    #Gestiona la conexión a la base de datos MySQL.

    def __init__(self):
        self.host = str(os.getenv("DB_HOST","localhost"))
        self.name = str(os.getenv("DB_NAME",""))
        self.user = str(os.getenv("DB_USER","root"))
        self.passwd = str(os.getenv("DB_PASSWORD",""))
        self.port = int(os.getenv("DB_PORT", "3306"))

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
                    charset='utf8mb4',
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
    return _ejecutar_query(query, params, fetch_mode='all') # type: ignore


def ejecutar_consulta_uno(query: str, params=None) -> dict | None:
    return _ejecutar_query(query, params, fetch_mode='one') # type: ignore


def ejecutar_insercion(query: str, params=None) -> int:
    """Ejecuta INSERT y retorna el ID insertado"""
    return _ejecutar_query(query, params, fetch_mode='none') # type: ignore


def ejecutar_actualizacion(query: str, params=None) -> int:
    """Ejecuta UPDATE/DELETE y retorna filas afectadas"""
    return _ejecutar_query(query, params, fetch_mode='none') # type: ignore