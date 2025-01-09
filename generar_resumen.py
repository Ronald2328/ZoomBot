import os
import openai
from guardar_transcripciones import leer_reuniones
from ZendeskConfig import ZendeskConfig
from fpdf import FPDF

ZendeskConfig = ZendeskConfig()
openai.api_key = ZendeskConfig.get_openai_key()

def leer_transcripcion(nombre_archivo):
    """
    Lee la transcripción desde un archivo de texto.

    Parámetros:
    nombre_archivo (str): Ruta del archivo que contiene la transcripción.

    Retorna:
    str: El contenido de la transcripción.
    """
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return archivo.read()

def resumir_transcripcion(transcripcion, max_tokens=500, temperatura=0.4):
    """
    Utiliza la API de OpenAI para generar un resumen de la transcripción.

    Parámetros:
    transcripcion (str): El texto de la transcripción.
    max_tokens (int): El número máximo de tokens para el resumen.
    temperatura (float): Controla la aleatoriedad en la generación.

    Retorna:
    dict: Un diccionario estructurado con el resumen detallado.
    """
    prompt = (
        "Eres un asistente experto en análisis y redacción de resúmenes. "
        "Tu tarea es procesar la transcripción que te proporciono y resumirla de manera clara y concisa. "
        "Identifica los roles de los participantes basándote en lo que mencionan, como líder, desarrollador, analista, etc. "
        "Sigue este esquema detallado para el resumen:\n"
        "1. **Personas que asistieron:** (nombre y roles asignados basados en sus aportes).\n"
        "2. **Objetivos de la reunión:** (describe el propósito principal).\n"
        "3. **Puntos clave discutidos:** (incluye temas importantes).\n"
        "4. **Decisiones tomadas:** (conclusiones, acuerdos o tareas asignadas).\n\n"
        "Aquí está la transcripción:\n"
        f"{transcripcion}\n\n"
        "Por favor, organiza la información según el esquema y proporciona un resumen claro y estructurado."
    )

    try:
        respuesta = openai.Completion.create(
            engine="text-davinci-003",  # Modelo para texto avanzado
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperatura,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        resumen_texto = respuesta.choices[0].text.strip()

        # Estructurar el resumen como un diccionario para mayor versatilidad
        return {
            "Personas que asistieron": "Extraído del resumen:\n" + resumen_texto.split("**Objetivos de la reunión:**")[0].strip(),
            "Objetivos de la reunión": resumen_texto.split("**Objetivos de la reunión:**")[1].split("**Puntos clave discutidos:**")[0].strip(),
            "Puntos clave discutidos": resumen_texto.split("**Puntos clave discutidos:**")[1].split("**Decisiones tomadas:**")[0].strip(),
            "Decisiones tomadas": resumen_texto.split("**Decisiones tomadas:**")[1].strip(),
        }
    except Exception as e:
        print(f"Error al generar el resumen: {e}")
        return None
    
def exportar_a_pdf(resumen, ruta_pdf):
    """
    Exporta un resumen estructurado a un archivo PDF.

    Parámetros:
    resumen (dict): Resumen estructurado con claves para cada sección.
    ruta_pdf (str): Ruta completa del archivo PDF a guardar.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style="B", size=14)
    pdf.cell(200, 10, txt="Resumen de la reunión", ln=True, align="C")
    pdf.ln(10)  # Espacio extra

    # Agregar secciones
    for titulo, contenido in resumen.items():
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt=titulo, ln=True, align="L")
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, contenido)
        pdf.ln(5)

    # Guardar PDF
    pdf.output(ruta_pdf)
    print(f"Resumen exportado a PDF: {ruta_pdf}")

def guardar_resumen(resumen, nombre_archivo, formato="pdf"):
    """
    Guarda el resumen en un archivo, ya sea en formato PDF o texto.

    Parámetros:
    resumen (dict): Resumen estructurado con claves para cada sección.
    nombre_archivo (str): Nombre del archivo sin ruta.
    formato (str): El formato en el que se guardará el archivo ('pdf' o 'txt').
    """
    os.makedirs("resumenes", exist_ok=True)
    ruta_completa = os.path.join("resumenes", nombre_archivo)

    if formato == "pdf":
        # Generar un PDF desde el resumen estructurado
        exportar_a_pdf(resumen, ruta_completa)
    elif formato == "txt":
        # Guardar en un archivo de texto plano
        with open(ruta_completa, "w", encoding="utf-8") as archivo:
            for titulo, contenido in resumen.items():
                archivo.write(f"{titulo}:\n{contenido}\n\n")
        print(f"Resumen guardado en texto: {ruta_completa}")
    else:
        print("Formato no soportado. Usa 'pdf' o 'txt'.")

def generar_resumenes_faltantes():
    """
    Genera resúmenes para las transcripciones ya guardadas en la carpeta.
    """
    reuniones = leer_reuniones()
    
    for reunion in reuniones:
        fecha = f"{reunion['Anio']}-{reunion['Mes']}-{reunion['Dia']}"
        asunto = reunion["Comentario"].replace(" ", "_")
        nombre_archivo_transcripcion = f"transcripciones/{fecha}_{asunto}.txt"
        nombre_archivo_resumen = f"resumenes/{fecha}_{asunto}.txt"

        # Verificar si ya existe un resumen
        if os.path.exists(nombre_archivo_resumen):
            print(f"Resumen ya existe para la reunión: {asunto} en {fecha}. Se omite.")
            continue

        # Leer la transcripción
        if os.path.exists(nombre_archivo_transcripcion):
            transcripcion = leer_transcripcion(nombre_archivo_transcripcion)

            # Generar el resumen
            resumen = resumir_transcripcion(transcripcion)

            # Guardar el resumen si fue generado
            if resumen:
                guardar_resumen(resumen, nombre_archivo_resumen)
                print(f"Resumen guardado para la reunión: {asunto} en {fecha}.")
        else:
            print(f"No se encontró la transcripción para la reunión: {asunto} en {fecha}.")
            