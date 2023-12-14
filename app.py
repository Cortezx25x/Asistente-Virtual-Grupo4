from flask import Flask, render_template, request, jsonify
import os
import subprocess
from action import accion
import speech_recognition as sr
from pytorch import hacer_pregunta

app = Flask(__name__)

AUDIO_UPLOAD_FOLDER = os.path.join(os.getcwd(), "audio_uploads")
ffmpeg_path = "C:/webm/bin/ffmpeg.exe" 

if not os.path.exists(AUDIO_UPLOAD_FOLDER):
    os.makedirs(AUDIO_UPLOAD_FOLDER)

def convert_audio_to_wav(input_file, output_file):
    command = [ffmpeg_path, "-y", "-i", input_file, "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_file]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Error al ejecutar FFmpeg:", e)
        raise


@app.route("/")
def index():
    return render_template("recorder.html")


@app.route('/audio', methods=['POST'])
def handle_audio():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        filename = os.path.join(AUDIO_UPLOAD_FOLDER, "temp_audio.webm")
        audio_file.save(filename)
        converted_filename = os.path.join(AUDIO_UPLOAD_FOLDER, "temp_audio.wav")
        
        if os.path.exists(filename):
            convert_audio_to_wav(filename, converted_filename)
        else:
            print("El archivo de entrada no existe:", filename)

        convert_audio_to_wav(filename, converted_filename)
        recognizer = sr.Recognizer()
        with sr.AudioFile(converted_filename) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language='es-ES')
            except sr.UnknownValueError:
                return jsonify({'error': 'No se pudo transcribir el audio'}), 400

        os.remove(filename)  
        os.remove(converted_filename)   
        
        text_lower = text.lower()
        if "alexa" in text_lower:
            
            texto = accion(text_lower)      
            return jsonify({'text': texto})
        

        return jsonify({'text': text})
    else:
        return jsonify({'error': 'No se encontró archivo de audio'}), 400

if __name__ == '__main__':
    app.run(debug=True)
