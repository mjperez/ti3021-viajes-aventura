import os

def validar_opcion(opcion, min, max) -> bool:
    #Valida entrada del usuario
    if not isinstance(opcion,int) and not isinstance(min,int) and not isinstance(max,int):
        print("La opción y los minimos y máximos deben ser numeros.")
        return False
    return min < opcion < max

def limpiar_pantalla():
    #Limpia la consola
    os.system("cls")

def pausar():
    #Espera input del usuario antes de continuar
    input("Presione Enter para continuar...")