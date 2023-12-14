import requests
from datetime import datetime
import pytz

def obtener_fecha_hora_actual(zona_horaria="Etc/GMT-6"):
    url = f"http://worldtimeapi.org/api/timezone/{zona_horaria}"
    respuesta = requests.get(url)
    tz = pytz.timezone(zona_horaria)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        fecha = fecha_hora_actual = datetime.now(tz)
        return fecha
    else:
        return None

def analizar_texto_y_responder(texto):
    texto = texto.lower()
    fecha =""
    fecha_hora_actual = obtener_fecha_hora_actual()

    if not fecha_hora_actual:
        return "No se pudo obtener la fecha y hora actual."

    if "fecha" in texto and "hora" in texto:
        fecha = fecha_hora_actual.strftime("La fecha es %Y-%m-%d y la hora es %H:%M:%S")
        return fecha
    elif "fecha" in texto:
        fecha = fecha_hora_actual.strftime("La fecha actual es %Y-%m-%d") 
        print(fecha)       
        return fecha
    elif "hora" in texto:
        fecha = fecha_hora_actual.strftime("La hora actual es %H:%M:%S")      
        return fecha
    else:
        return "No se ha solicitado ni la fecha ni la hora."
