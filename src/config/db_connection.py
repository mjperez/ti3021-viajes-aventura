"""Módulo de conexión a base de datos MySQL.

Gestiona la conexión a la base de datos MySQL usando PyMySQL.
Proporciona funciones helper para ejecutar consultas SQL.
"""

import os

import pymysql
from dotenv import load_dotenv

from src.utils import DB_CHARSET, DB_PORT_DEFAULT

_instancia_conexion = None
load_dotenv()


class Conexion():
    """Gestiona la conexión a la base de datos MySQL."""

    def __init__(self):
        self.host = str(os.getenv("DB_HOST", "localhost"))
        self.name = str(os.getenv("DB_NAME", ""))
        self.user = str(os.getenv("DB_USER", "root"))
        self.passwd = str(os.getenv("DB_PASSWORD", ""))
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
    """Obtiene la conexión a la base de datos."""
    global _instancia_conexion
    if _instancia_conexion is None:
        _instancia_conexion = Conexion()
    return _instancia_conexion._conectar()


def cerrar_conexion():
    """Cierra la conexión a la base de datos."""
    global _instancia_conexion
    if _instancia_conexion:
        _instancia_conexion._cerrar()
        _instancia_conexion = None


def _ejecutar_query(query: str, params=None, fetch_mode='all'):
    """Función privada para ejecutar queries."""
    conn = obtener_conexion()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        
        if fetch_mode == 'all':  # SELECT que retorna muchas filas
            return cursor.fetchall()
        elif fetch_mode == 'one':  # SELECT que retorna una sola fila
            return cursor.fetchone()
        elif fetch_mode == 'none':  # INSERT, UPDATE, DELETE
            conn.commit()
            # Si es INSERT (lastrow>0) retorna ID, si es UPDATE/DELETE (lastrow=0) retorna filas afectadas
            return cursor.lastrowid if cursor.lastrowid > 0 else cursor.rowcount 

    except pymysql.MySQLError as e:
        if fetch_mode == 'none':  # Si intentó modificar, rollback
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
    return _ejecutar_query(query, params, fetch_mode='all')  # type: ignore


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
    return _ejecutar_query(query, params, fetch_mode='one')  # type: ignore


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
    return _ejecutar_query(query, params, fetch_mode='none')  # type: ignore


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
    return _ejecutar_query(query, params, fetch_mode='none')  # type: ignore
