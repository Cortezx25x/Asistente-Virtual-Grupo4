from selenium import webdriver
from selenium.webdriver.edge.service import Service
import datetime
import time
from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError
from gtts import gTTS
from playsound import playsound
import random
import requests
from showEvents import main
from createEvents import recordatorio
from auth import authentication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from goslate import traductorEN, traductorES
from gpt import chatgpt


#DECLARAR VARIABLES UNIVERSALES
validaAuth = False
browser = webdriver


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

def escribir(texto):
    print("escribiendo...")
    cajitaDeTexto = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    cajitaDeTexto.send_keys(texto)

def enviar():
    print("enviado...")
    enviar = browser.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]')
    enviar.click()

def bootWhatsapp():
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

def activarAsistente():
    escuchar()
    while True:
        time.sleep(1)

def escuchar():
    print("Escuchando...")
    recognizer =  Recognizer()
    microfono =  Microphone()

    with microfono:
        recognizer.adjust_for_ambient_noise(microfono)
    
    recognizer.listen_in_background(microfono,callback)

def callback(recognizer, source):
    print("Reconociendo...")

    try:
        reconocer = recognizer.recognize_google(source, language='es-ES')
        texto = str(reconocer).lower()
        print("Escuche : ", texto)
        if(texto.__contains__("alexa")):
            print("Llamo a alexa")
            accion(texto)
        return

    except RequestError as exc:
        print("Error al escuhar : ", exc)
    except UnknownValueError:
        print("No entendí")
        #playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/errorRespuesta.mp3')
        time.sleep(1)

def accion(texto: str):

    print("Reconociendo accion...")
    

    if(texto.__contains__("abrir whatsapp")):
        print("Abriendo whatsapp...")
       # playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/abrirwts.mp3')
        time.sleep(1)
        global browser
        service = Service(executable_path='./edgedriver_win64/edgedriver.exe')
        browser = webdriver.Edge(service=service)
        bootWhatsapp()

    if(texto.__contains__("enviar mensaje a")):
        if(validaAuth == False):
            
            print("Autenticate por favor")
            playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/abrirwts.mp3')
            time.sleep(1)
            return
        
        texto = texto.replace("enviar mensaje a", "")
        buscarChat(texto)
        return
    
    if(texto.__contains__("escribir")):
        texto = texto.replace("escribir", "")
        escribir(texto)
        return

    if(texto.__contains__("enviar")):
       enviar()
       return

    if(texto.__contains__("cuenta un chiste")):
        chiste()
        return
    
    if(texto.__contains__("ver eventos")):
        main()
        return
    
    if(texto.__contains__("crear evento")):
        recordatorio()
        return
    
    if(texto.__contains__("cerrar explorador")):
        print("cerrando browser...")
        browser.close()
        return
    
    if(texto.__contains__("Salir")):
        print("Sistema: ¡Hasta luego!")
        return    
    
    else:
        
        chatgpt()
    
    print("Accion no encontrada...")
    return

def chiste():
    print("CONTANDO CHISTE...")
    aleatorio = random.randrange(10)
    
    print("CONTANDO CHISTE : ", str(aleatorio))

    if(aleatorio == 1):
     #playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/obligame.mp3')
      playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/chiste1.mp3')
    else:
      playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/chiste2.mp3')
    
    time.sleep(1)
    return

def hablar(texto: str):
    print("Hablando...")
    audio = gTTS(text=texto,lang='es-us',slow=False)
    #audio.save('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/obligame.mp3')
    #time.sleep(1)
    playsound('C:/Users/Cortez/Desktop/AsistenteVirtual-master/AsistenteVirtual-master/resource/chiste1.mp3')
    return

activarAsistente() 
#hablar('obligame perro')