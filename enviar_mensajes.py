from datetime import datetime, timedelta
from generar_enlaces import leer_contactos, leer_reuniones
from generar_mensajes_zoom import generar_mensajes

def filtrar_reuniones_proximas(reuniones, horas):
    """
    Filtra las reuniones que ocurrirán dentro de un rango de horas especificado desde el momento actual.

    Parámetros:
    reuniones (list): Una lista de diccionarios, donde cada diccionario contiene la información de una reunión.
    horas (int): El número de horas desde el momento actual para considerar las reuniones próximas.

    Retorna:
    list: Una lista de diccionarios con las reuniones que ocurrirán dentro del rango de horas especificado.
    """
    fecha_actual = datetime.now()
    fecha_limite = fecha_actual + timedelta(hours=horas)
    
    reuniones_proximas = []
    for reunion in reuniones:
        fecha_reunion = datetime(int(reunion['Anio']), int(reunion['Mes']), int(reunion['Dia']),
                                 int(reunion['HoraEn24H'].split(':')[0]), int(reunion['HoraEn24H'].split(':')[1]))
        if fecha_actual <= fecha_reunion <= fecha_limite:
            reuniones_proximas.append(reunion)
    
    return reuniones_proximas

def notificar_reuniones_proximas(horas):
    """
    Notifica a los contactos sobre las reuniones próximas que ocurrirán dentro de un rango de horas especificado.

    Parámetros:
    horas (int): El número de horas desde el momento actual para considerar las reuniones próximas.
    """
    reuniones = leer_reuniones()
    contactos = leer_contactos()
    
    reuniones_proximas = filtrar_reuniones_proximas(reuniones, horas)
    
    for contacto in contactos:
        nombre_contacto = contacto['Nombre']
        
        reuniones_relevantes = [reunion for reunion in reuniones_proximas]
        
        if reuniones_relevantes:
            mensaje = generar_mensajes(nombre_contacto ,reuniones_relevantes) 
            
            if mensaje:
                print(f"Enviando mensaje a {contacto['Nombre']} a su número {contacto['Telefono']}: \n{mensaje}")
                