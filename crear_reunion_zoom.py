import requests

def crear_reunion_zoom(user_id, access_token, topic, 
                       start_time, duration, password="123456", 
                       agenda="", timezone="America/Los_Angeles"):
    """
    Crea una reunión de Zoom utilizando la API de Zoom y devuelve el enlace para unirse, el ID de la reunión y la contraseña.

    Args:
        user_id (str): El ID del usuario o el valor "me" para el usuario autenticado.
        access_token (str): El token de acceso para autenticar la solicitud.
        topic (str): El tema de la reunión.
        start_time (str): La hora de inicio de la reunión en formato ISO 8601 (UTC).
        duration (int): La duración de la reunión en minutos.
        password (str, optional): La contraseña de la reunión. Por defecto es "123456".
        agenda (str, optional): La agenda de la reunión. Por defecto es una cadena vacía.
        timezone (str, optional): La zona horaria de la reunión. Por defecto es "America/Los_Angeles".

    Returns:
        dict: Un diccionario con la URL para unirse a la reunión, el ID de la reunión y la contraseña si la creación es exitosa, de lo contrario, un mensaje de error.
    """

    # URL para crear la reunión
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"

    # Construir el payload con la información de la reunión
    payload = {
        "topic": topic,                           # Título de la reunión
        "type": 2,                                # 2 para reuniones programadas
        "start_time": start_time,                 # Hora de inicio en formato ISO 8601
        "duration": duration,                     # Duración en minutos
        "timezone": timezone,                     # Zona horaria
        "password": password,                     # Contraseña de la reunión
        "agenda": agenda,                         # Agenda
        "settings": {
            "host_video": True,                   # Habilitar video del host
            "participant_video": True,            # Habilitar video de los participantes
            "mute_upon_entry": False,             # No silenciar al entrar
            "waiting_room": False,                # No activar sala de espera
            "registration_type": 1,               # 1 para requerir registro
        }
    }

    # Encabezados de la solicitud
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"  # Usar el token de acceso
    }

    # Realizar la solicitud POST
    response = requests.post(url, json=payload, headers=headers)

    # Verificar el resultado de la solicitud
    if response.status_code == 201:
        meeting_info = response.json()
        return {
            "join_url": meeting_info["join_url"],    # URL para unirse a la reunión
            "meeting_id": meeting_info["id"],        # ID de la reunión
            "password": meeting_info["password"]     # Contraseña de la reunión
        }
    else:
        return f"Error: {response.status_code}, {response.json()}"