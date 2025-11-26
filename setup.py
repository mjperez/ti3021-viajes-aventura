import os

import pymysql


def instalar_db():
    conexion = None
    cursor = None
    print("-- Inicializando el proyecto --")
    print("Para configurar la base de datos:")
    root_pass = input("Ingrese la contraseña de su usuario ROOT de MySQL:")

    try:
        conexion = pymysql.connect(
            host="localhost",
            user="root",
            password=root_pass,
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conexion.cursor()

        ruta_sql = os.path.join("database","init_db.sql")

        if not os.path.exists(ruta_sql):
            print(f"ERROR: No encuentro el archivo *.sql en {ruta_sql}")
            return
        
        with open(ruta_sql,"r",encoding="utf-8") as archivo:
            contenido_sql = archivo.read()
        
        comandos = contenido_sql.split(';')

        print("Ejecutando script SQL... Espere un momento.")
        for comando in comandos:
            comando_limpio = comando.strip()

            if comando_limpio:
                try:
                    cursor.execute(comando_limpio)
                except pymysql.Error as e:
                    # Ignoramos errores pequeños de "la tabla ya existe" o warnings
                    print(f"Nota: Hubo un detalle ejecutando: {comando_limpio[:50]}... -> {e}")
        conexion.commit()
        print("Base de datos, usuario y tablas creadas correctamente.")
        print("Ahora puedes ejecturar 'python main.py")

    except pymysql.Error as e:
        print(f"Error de MySQL: {e}")
        print("Verifica la contraseña de root y que MySQL este corriendo.")
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()

if __name__ == "__main__":
    instalar_db()
