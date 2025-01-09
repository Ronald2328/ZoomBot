import requests

class ZoomClient:
    """
    Clase para manejar la autenticación y obtener un token de acceso para la API de Zoom.

    Atributos:
    account_id (str): El ID de la cuenta de Zoom.
    client_id (str): El ID del cliente de Zoom.
    client_secret (str): El secreto del cliente de Zoom.
    access_token (str): El token de acceso obtenido después de la autenticación.

    Métodos:
    __init__(self, account_id, client_id, client_secret):
        Inicializa la clase ZoomClient con los datos de autenticación y obtiene el token de acceso.

    get_access_token(self):
        Realiza una solicitud a la API de Zoom para obtener un token de acceso utilizando las credenciales proporcionadas.
    """

    def __init__(self, account_id, client_id, client_secret) -> None:
        """
        Inicializa la clase ZoomClient con los datos de autenticación y obtiene el token de acceso.

        Parámetros:
        account_id (str): El ID de la cuenta de Zoom.
        client_id (str): El ID del cliente de Zoom.
        client_secret (str): El secreto del cliente de Zoom.
        """
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        Realiza una solicitud a la API de Zoom para obtener un token de acceso utilizando las credenciales proporcionadas.

        Retorna:
        str: El token de acceso obtenido de la API de Zoom.
        """
        data = {
            "grant_type": "account_credentials",
            "account_id": self.account_id,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post("https://zoom.us/oauth/token", data=data)
        return response.json()["access_token"]