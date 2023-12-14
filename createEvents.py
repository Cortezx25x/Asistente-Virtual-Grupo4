import datetime
from auth import authentication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dateutil import parser
from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError, RequestError
import re

# Configuración de la API y autenticación


# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.

creds = authentication()

def convertir_fecha_hora(texto_fecha_hora):
    try:
        return parser.parse(texto_fecha_hora)
    except ValueError:
        print("No se pudo interpretar la fecha/hora:", texto_fecha_hora)
        return None
    
    
def extract_event_details(transcribed_text):
    details = {
        "summary": "",
        "description": "",
        "start": {"dateTime": None, "timeZone": "America/Chicago"},
        "end": {"dateTime": None, "timeZone": "America/Chicago"}
    }

    title_match = re.search(r"Título del evento:\s*(.*)", transcribed_text)
    if title_match:
        details["summary"] = title_match.group(1)

    description_match = re.search(r"Descripción del evento:\s*(.*)", transcribed_text)
    if description_match:
        details["description"] = description_match.group(1)

    start_match = re.search(r"Fecha y hora de inicio:\s*(.*)", transcribed_text)
    if start_match:
        details["start"]["dateTime"] = parser.parse(start_match.group(1)).isoformat()

    end_match = re.search(r"Fecha y hora de fin:\s*(.*)", transcribed_text)
    if end_match:
        details["end"]["dateTime"] = parser.parse(end_match.group(1)).isoformat()

    return details



def create_google_calendar_event(creds, event_details):
    try:
        service = build("calendar", "v3", credentials=creds)
        event_result = service.events().insert(calendarId='primary', body=event_details).execute()
        print(f"Evento creado: {event_result.get('htmlLink')}")
    except Exception as e:
        print(f"Error al crear el evento: {e}")



def create_event(text):
    event_details = extract_event_details(text)
    create_google_calendar_event(creds, event_details)
    return event_details




def escuchar_para_datos(prompt):
    recognizer = Recognizer()
    print(prompt)
    with Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic)
        audio = recognizer.listen(mic)
    try:
        return recognizer.recognize_google(audio, language='es-ES').lower()
    except RequestError as exc:
        print("Error al escuchar: ", exc)
        return None
    except UnknownValueError:
        print("No entendí")
        return None
    
def crear_recordatorio():
        summary = escuchar_para_datos("Diga el título del evento:")
        if not summary:
            return escuchar_para_datos("Diga el título del evento:")

        description = escuchar_para_datos("Diga la descripción del evento:")
        if not description:
            return escuchar_para_datos("Diga la descripción del evento:")

        start = escuchar_para_datos("Diga la fecha de inicio con formato año-mes-día hora:minuto:")
        if not start:
            return escuchar_para_datos("Diga la fecha de inicio con formato año-mes-día hora:minuto:")

        end = escuchar_para_datos("Diga la fecha de fin con formato año-mes-día hora:minuto:")
        if not end:
            return escuchar_para_datos("Diga la fecha de fin con formato año-mes-día hora:minuto:")

        start = convertir_fecha_hora(start)
        end = convertir_fecha_hora(end)
        
        recordatorio(summary, description, start, end)
    
    
def recordatorio(summary,description,start,end):
    try:
        service = build("calendar", "v3", credentials=creds)
        
        event = {
        'summary': summary,
        'location': '',
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/Chicago',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }
        
        
        events_result = (
            service.events()
            .insert(
                calendarId="primary",
                body=event,
            )
            .execute()
        )
        
        print ('Event created: %s' % (event.get('htmlLink')))

        
    except HttpError as error:
        print(f"An error occurred: {error}")