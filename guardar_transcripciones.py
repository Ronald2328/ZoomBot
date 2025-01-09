import requests
import os
from generar_enlaces import leer_reuniones

def obtener_transcripcion(meeting_id, access_token):
    """
    Obtiene la transcripción de una reunión de Zoom.

    Parámetros:
    meeting_id (str): El ID de la reunión.
    access_token (str): El token de acceso para autenticar la solicitud.

    Retorna:
    str: La transcripción de la reunión si está disponible, o None si ya está guardada.
    """
    url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        recordings = response.json().get("recording_files", [])
        for file in recordings:
            if file.get("file_type") == "TRANSCRIPT":
                transcript_url = file.get("download_url")
                transcript_response = requests.get(transcript_url, headers=headers)
                if transcript_response.status_code == 200:
                    return transcript_response.text
    return None  # Devuelve None si no hay transcripción disponible

def guardar_transcripcion(reunion, transcripcion):
    """
    Guarda la transcripción de una reunión en un archivo.

    Parámetros:
    reunion (dict): Información de la reunión, incluyendo la fecha y el tema.
    transcripcion (str): El texto de la transcripción.
    """
    fecha = f"{reunion['Anio']}-{reunion['Mes']}-{reunion['Dia']}"
    asunto = reunion["Comentario"].replace(" ", "_")
    nombre_archivo = f"transcripciones/{fecha}_{asunto}.txt"

    os.makedirs("transcripciones", exist_ok=True)
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(transcripcion)

def procesar_transcripciones(access_token):
    """
    Procesa las reuniones para obtener y guardar sus transcripciones.

    Parámetros:
    access_token (str): El token de acceso para autenticar las solicitudes.
    """
    reuniones = leer_reuniones()
    for reunion in reuniones:
        meeting_id = reunion.get("IDreunione")
        if meeting_id:
            fecha = f"{reunion['Anio']}-{reunion['Mes']}-{reunion['Dia']}"
            asunto = reunion["Comentario"].replace(" ", "_")
            nombre_archivo = f"transcripciones/{fecha}_{asunto}.txt"

            # Comprueba si la transcripción ya ha sido guardada
            if os.path.exists(nombre_archivo):
                print(f"La transcripción ya existe: {nombre_archivo}")
                continue  # Si ya existe, pasa a la siguiente reunión

            transcripcion = obtener_transcripcion(meeting_id, access_token)
            if transcripcion:
                guardar_transcripcion(reunion, transcripcion)
            else:
                print(f"No se encontró una transcripción para la reunión: {meeting_id}")
