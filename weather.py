import requests

# Clave API de OpenWeatherMap 
API_KEY = "f410105ce618e56262dd7374502971dd"

def extraer_ciudad_de_texto(texto):
    palabras = texto.split()
    if "clima" in palabras and "en" in palabras:
        indice = palabras.index("en")
        if indice + 1 < len(palabras):
            return palabras[indice + 1]
    return None

def obtener_clima(texto_usuario):
    ciudad = extraer_ciudad_de_texto(texto_usuario)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={API_KEY}&units=metric"
    respuesta = requests.get(url)
    if respuesta.status_code == 200:
        datos = respuesta.json()
        clima = datos['weather'][0]['description']
        temperatura = datos['main']['temp']
        respuesta = f"El clima en {ciudad} es: {clima} con una temperatura de {temperatura}°C"
        return respuesta
    else:
        return "No se pudo obtener el clima."
