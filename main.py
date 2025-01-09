from ZendeskConfig import ZendeskConfig
from ZoomClient import ZoomClient
from generar_enlaces import completar_reuniones
from enviar_mensajes import notificar_reuniones_proximas
from generar_resumen import generar_resumenes_faltantes

ZendeskConfig = ZendeskConfig()
ZOOM_ACCOUNT_ID = ZendeskConfig.get_account_id()
ZOOM_CLIENT_ID = ZendeskConfig.get_client_id()
ZOOM_CLIENT_SECRET = ZendeskConfig.get_client_secret()

client = ZoomClient(account_id=ZOOM_ACCOUNT_ID, 
                    client_id=ZOOM_CLIENT_ID, 
                    client_secret=ZOOM_CLIENT_SECRET)

access_token = client.get_access_token()

completar_reuniones(access_token = access_token, 
                    user_id = "me")

notificar_reuniones_proximas(horas=24)

generar_resumenes_faltantes()