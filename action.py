from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import time
from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError
from gtts import gTTS
from playsound import playsound
from weather import obtener_clima
from showEvents import mostrarEventos
from createEvents import crear_recordatorio
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from gpt import chatgpt
from worldTime import analizar_texto_y_responder
from createEvents import create_event

validaAuth = False
escuchando = True 
browser = webdriver

#WhatsApp
def validaQR():
    try:
        element = browser.find_element_by_tag_name("canvas")
    except:
        return False
    return True

def buscarChat(nombreChat : str):
    print("BUSCANDO CHAT : ", nombreChat)
    elements = browser.find_elements_by_tag_name("span")
    for element in elements:
        print("CHAT ENCONTRADO : " + str(element.text).lower())
        if element.text !='' and nombreChat.__contains__(str(element.text).lower()):
            element.click()
            return
    print("NO ENCONTRO CHAT")

def enviar():
    print("enviado...")
    enviar = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
    enviar.click()

def bootWhatsapp():
    path_to_geckodriver = 'C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/geckodriver-v0.33.0-win64/geckodriver.exe'
    service = Service(executable_path=path_to_geckodriver)
    browser = webdriver.Firefox(service=service)
    browser.get("https://web.whatsapp.com/")
    time.sleep(5)

    espera = True
    print("AUTENTICATE POR FAVOR")

    while espera:
        espera = validaQR()
        time.sleep(2)
        if espera == False:
            global validaAuth
            validaAuth = True
            print("SE AUTENTICO")
            break
        

def accion(texto: str):
    global browser
    print("Reconociendo accion...")
    
    if texto.__contains__("abrir whatsapp"):
        respuesta = "Abriendo whatsapp..."
        time.sleep(1)
        bootWhatsapp()
        return respuesta
    
    if(texto.__contains__("enviar mensaje a")):
        if(validaAuth == False):
            
            print("Autenticate por favor")
            playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/abrirwts.mp3')
            time.sleep(1)
            return
        
        texto = texto.replace("enviar mensaje a", "")
        buscarChat(texto)
        return

    if(texto.__contains__("enviar")):
       enviar()
       return

    if(texto.__contains__("ver eventos")):
        respuesta = mostrarEventos()
        return respuesta
    
    if (texto.__contains__("crear evento")):
        create_event(texto)
        respuesta = "Evento Creado Correctamente"
        return respuesta
        
    if (texto.__contains__("clima")):
        obtener_clima(texto)
        
    if "fecha" in texto or "hora" in texto:
        respuesta = analizar_texto_y_responder(texto)
        return respuesta
                     
    if(texto.__contains__("cerrar explorador")):
        print("cerrando browser...")
        browser.close()
        return
    else:
       respuesta = chatgpt(texto)    
       return respuesta
    

def hablar(texto: str):
    print("Hablando...")
    audio = gTTS(text=texto,lang='es-us',slow=False)
    #audio.save('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/obligame.mp3')
    #time.sleep(1)
    playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/chiste1.mp3')
    return


