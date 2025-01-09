import json
import os

class ZendeskConfig:
    """
    Clase para manejar la configuración de Zendesk a partir de un archivo de secretos en formato JSON.

    Atributos:
    secrets_file (str): La ruta del archivo JSON que contiene los secretos. Por defecto es 'secrets.json'.
    config (dict): Diccionario que contiene la configuración cargada desde el archivo de secretos.

    Métodos:
    __init__(self, secrets_file='secrets.json'):
        Inicializa la clase ZendeskConfig con el archivo de secretos especificado.

    _load_secrets(self):
        Carga los secretos desde el archivo JSON especificado. Si el archivo no existe, lanza una excepción FileNotFoundError.

    get_account_id(self):
        Devuelve el ID de la cuenta de Zendesk desde la configuración cargada.

    get_client_id(self):
        Devuelve el ID del cliente de Zendesk desde la configuración cargada.

    get_client_secret(self):
        Devuelve el secreto del cliente de Zendesk desde la configuración cargada.

    get_token(self):
        Devuelve el token de Zendesk desde la configuración cargada.

    get_verification_token(self):
        Devuelve el token de verificación de Zendesk desde la configuración cargada.
    """

    def __init__(self, secrets_file='secrets.json'):
        """
        Inicializa la clase ZendeskConfig con el archivo de secretos especificado.

        Parámetros:
        secrets_file (str): La ruta del archivo JSON que contiene los secretos. Por defecto es 'secrets.json'.
        """
        self.secrets_file = secrets_file
        self.config = self._load_secrets()

    def _load_secrets(self):
        """
        Carga los secretos desde el archivo JSON especificado.

        Retorna:
        dict: Un diccionario con la configuración cargada desde el archivo de secretos.

        Excepciones:
        FileNotFoundError: Si el archivo de secretos no existe.
        """
        if not os.path.exists(self.secrets_file):
            raise FileNotFoundError(f"El archivo {self.secrets_file} no existe.")
        with open(self.secrets_file, 'r') as file:
            return json.load(file)

    def get_account_id(self):
        """
        Devuelve el ID de la cuenta de Zendesk desde la configuración cargada.

        Retorna:
        str: El ID de la cuenta de Zendesk.
        """
        return self.config['zendesk']['Account ID']

    def get_client_id(self):
        """
        Devuelve el ID del cliente de Zendesk desde la configuración cargada.

        Retorna:
        str: El ID del cliente de Zendesk.
        """
        return self.config['zendesk']['Client ID']

    def get_client_secret(self):
        """
        Devuelve el secreto del cliente de Zendesk desde la configuración cargada.

        Retorna:
        str: El secreto del cliente de Zendesk.
        """
        return self.config['zendesk']['Client Secret']

    def get_token(self):
        """
        Devuelve el token de Zendesk desde la configuración cargada.

        Retorna:
        str: El token de Zendesk.
        """
        return self.config['zendesk']['Token']

    def get_verification_token(self):
        """
        Devuelve el token de verificación de Zendesk desde la configuración cargada.

        Retorna:
        str: El token de verificación de Zendesk.
        """
        return self.config['zendesk']['Verification Token']
    
    def get_openai_key(self):
        """
        Devuelve la clave de OpenAI desde la configuración cargada.

        Retorna:
        str: La clave de OpenAI.
        """
        return self.config['openai']['key_openAI']