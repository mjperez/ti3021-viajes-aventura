import os
import pymysql
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión para RESTAURACIÓN (debe ser un usuario con privilegios globales, e.g. root)
# NOTA: Ignoramos el usuario del .env (que suele ser el de la App) y usamos root por defecto para mantenimiento.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_ADMIN_USER", "root") 
DB_PASS = os.getenv("DB_ADMIN_PASSWORD", "") # WampServer por defecto no tiene password en root
DB_PORT = int(os.getenv("DB_PORT", "3306"))

SQL_FILE = os.path.join("database", "init_db.sql")

def reset_database():
    """
    Lee el archivo init_db.sql y ejecuta cada comando SQL.
    Se conecta sin seleccionar base de datos inicialmente para poder ejecutar DROP/CREATE DATABASE.
    """
    print("="*60)
    print("SCRIPT DE RESTAURACIÓN DE BASE DE DATOS")
    print("="*60)
    
    if not os.path.exists(SQL_FILE):
        print(f"Error: No se encuentra el archivo {SQL_FILE}")
        return

    print(f"1. Leyendo archivo SQL: {SQL_FILE}")
    try:
        with open(SQL_FILE, "r", encoding="utf-8") as f:
            sql_content = f.read()
    except Exception as e:
        print(f"Error leyendo archivo: {e}")
        return

    print("2. Conectando a MySQL...")
    try:
        # Conectar sin DB específica para permitir DROP/CREATE
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            port=DB_PORT,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.MySQLError as e:
        print(f"Error de conexión: {e}")
        print("Verifique que WampServer/MySQL esté corriendo y las credenciales en .env sean correctas.")
        return

    try:
        with conn.cursor() as cursor:
            print("3. Ejecutando sentencias SQL...")
            
            # Separar por punto y coma. 
            # NOTA: Esto asume que no hay ';' dentro de strings en el SQL simplificado.
            # Si el SQL se vuelve complejo con triggers/procedures, este método deberá mejorarse.
            statements = sql_content.split(';')
            
            for statement in statements:
                stmt = statement.strip()
                if stmt: # Si no está vacío
                    try:
                        cursor.execute(stmt)
                        # Mostrar progreso resumido
                        first_line = stmt.split('\n')[0]
                        if len(first_line) > 60:
                            first_line = first_line[:57] + "..."
                        print(f"   ✓ Ejecutado: {first_line}")
                    except Exception as e:
                        print(f"   ✗ Error en: {stmt[:50]}...")
                        print(f"     Detalle: {e}")
                        # Decidir si abortar o continuar. 
                        # DROP USER/DB IF EXISTS pueden fallar por permisos, pero si fallan queries críticos mejor detenerse.
                        ans = input("     ¿Desea continuar con la siguiente sentencia? (s/n): ")
                        if ans.lower() != 's':
                            raise e
        
        conn.commit()
        print("\n" + "="*60)
        print("¡BASE DE DATOS RESTAURADA EXITOSAMENTE!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
    except Exception as e:
        print(f"\nProceso interrumpido: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    reset_database()
