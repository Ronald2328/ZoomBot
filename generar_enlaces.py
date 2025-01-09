import csv
from datetime import datetime, timedelta
from crear_reunion_zoom import crear_reunion_zoom

def leer_contactos(ruta_archivo = 'contactos.csv'):
    """
    Lee un archivo CSV de contactos y devuelve una lista de diccionarios con la información de cada contacto.

    Parámetros:
    ruta_archivo (str): La ruta del archivo CSV que contiene los contactos. Por defecto es 'contactos.csv'.

    Retorna:
    list: Una lista de diccionarios, donde cada diccionario contiene la información de un contacto.

    Manejo de errores:
    - Si el archivo no se encuentra, imprime un mensaje de error indicando que el archivo no se encontró.
    - Si ocurre cualquier otro error durante la lectura del archivo, imprime un mensaje de error con la descripción del error.
    """
    contactos = []
    try:
        with open(ruta_archivo, 'r', newline='', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            contactos = [fila for fila in lector]
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    return contactos

def leer_reuniones(ruta_archivo='reuniones.csv'):
    """
    Lee un archivo CSV de reuniones y devuelve una lista de diccionarios con la información de cada reunión.

    Parámetros:
    ruta_archivo (str): La ruta del archivo CSV que contiene las reuniones. Por defecto es 'reuniones.csv'.

    Retorna:
    list: Una lista de diccionarios, donde cada diccionario contiene la información de una reunión.

    Manejo de errores:
    - Si el archivo no se encuentra, imprime un mensaje de error indicando que el archivo no se encontró.
    - Si ocurre cualquier otro error durante la lectura del archivo, imprime un mensaje de error con la descripción del error.
    """
    reuniones = []
    try:
        with open(ruta_archivo, 'r') as archivo:
            lector = csv.DictReader(archivo)
            reuniones = [fila for fila in lector]
    except FileNotFoundError:
        print(f"El archivo {ruta_archivo} no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    return reuniones

def escribir_reuniones(reuniones):
    """
    Escribe una lista de diccionarios en un archivo CSV.

    Parámetros:
    ruta_archivo (str): La ruta del archivo CSV donde se escribirán las reuniones.
    reuniones (list): Una lista de diccionarios, donde cada diccionario contiene la información de una reunión.

    Manejo de errores:
    - Si ocurre cualquier error durante la escritura del archivo, imprime un mensaje de error con la descripción del error.
    """
    try:
        encabezados = reuniones[0].keys()
        with open('reuniones.csv', 'w', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=encabezados)
            escritor.writeheader()
            escritor.writerows(reuniones)
    except Exception as e:
        print(f"Ocurrió un error al escribir el archivo: {e}")

def completar_reuniones(access_token, user_id):
    """
    Completa la información de las reuniones en un archivo CSV creando reuniones de Zoom
    únicamente para aquellas que no tienen enlace.

    Parámetros:
    ruta_archivo (str): La ruta del archivo CSV que contiene las reuniones.
    access_token (str): El token de acceso para la API de Zoom.
    user_id (str): El ID del usuario de Zoom.

    Manejo de errores:
    - Si ocurre cualquier error durante la lectura o escritura del archivo, imprime un mensaje de error con la descripción del error.
    """
    reuniones = leer_reuniones()
    for reunion in reuniones:
        if not reunion["Enlace"]: 
            topic = reunion["Comentario"]
            anio, mes, dia = int(reunion["Anio"]), int(reunion["Mes"]), int(reunion["Dia"])
            hora = datetime.strptime(reunion["HoraEn24H"], "%H:%M")
            start_time = datetime(anio, mes, dia, hora.hour, hora.minute) - timedelta(hours=5)  # Convertir a UTC
            start_time_iso = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
            duration = int(reunion["Duracion(En minutos)"])

            resultado = crear_reunion_zoom(user_id, access_token, topic, start_time_iso, duration)
            if isinstance(resultado, dict):
                reunion["IDreunione"] = resultado["meeting_id"]
                reunion["Contra"] = resultado["password"]
                reunion["Enlace"] = resultado["join_url"]
            else:
                print(f"No se pudo crear la reunión: {resultado}")
    
    escribir_reuniones(reuniones)
