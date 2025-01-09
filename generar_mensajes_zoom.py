def generar_mensajes(Nombre, reuniones_relevantes):
    """
    Genera mensajes formateados profesionalmente con los datos de reuniones relevantes.

    Args:
        Nombre (str): Nombre de la persona a la que se envía el mensaje.
        reuniones_relevantes (list): Lista de diccionarios con la información de las reuniones relevantes.

    Returns:
        str: Un string con los mensajes formateados, separados por líneas en blanco.
    """
    mensajes = []
    
    for reunion in reuniones_relevantes:
        mensaje = (
            f"📢 *Invitación a Reunión Programada*\n\n"
            f"Estimado/a {Nombre},\n\n"
            f"Tenemos el agrado de invitarle a la siguiente reunión:\n\n"
            f"📅 *Detalles de la Reunión:*\n"
            f"  - 🗓 *Fecha:* {reunion['Dia']}/{reunion['Mes']}/{reunion['Anio']}\n"
            f"  - ⏰ *Hora:* {reunion['HoraEn24H']} (hora peruana)\n"
            f"  - 🆔 *ID de la reunión:* {reunion['IDreunione']}\n"
            f"  - 🔑 *Contraseña:* {reunion['Contra']}\n"
            f"  - ⏳ *Duración:* {reunion['Duracion(En minutos)']} minutos\n\n"
            f"💡 *Tema:* {reunion['Comentario']}\n"
            f"🔗 *Enlace para unirse:* {reunion['Enlace']}\n\n"
            f"🔔 *Notas importantes:*\n"
            f"  1. Por favor, acceda al enlace 5 minutos antes para evitar inconvenientes.\n"
            f"  2. Asegúrese de tener una conexión estable.\n"
            f"  3. Si tiene dudas, no dude en decirlas.\n\n"
            f"¡Gracias por su atención y participación!\n"
        )
        mensajes.append(mensaje)

    return "\n\n".join(mensajes) if mensajes else "No hay reuniones relevantes para mostrar."
