import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import spacy
from goslate import traductorES, traductorEN

nltk.download('punkt')
nltk.download('stopwords')

model_name = "gpt2"
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

nlp_spacy = spacy.load("es_core_news_sm")

def preprocesar_texto(texto):
    # Tokenización con NLTK
    tokens = word_tokenize(texto)

    stop_words = set(stopwords.words('spanish'))
    tokens = [word for word in tokens if word.lower() not in stop_words]

    doc = nlp_spacy(" ".join(tokens))
    lemmatized_tokens = [token.lemma_ for token in doc]


    return lemmatized_tokens
# Función para generar texto
def generar_texto(seed_text, max_length=50, temperature=0.9):
    input_ids = tokenizer.encode(seed_text, return_tensors="pt")

    output = model.generate(
        input_ids,
        max_length=max_length,
        temperature=temperature,
        num_beams=5,
        no_repeat_ngram_size=2,
        top_k=50,
        top_p=0.95,
        pad_token_id=tokenizer.eos_token_id,
    )

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    return generated_text

def procesar_entrada_respuesta(entrada_usuario):
    entrada_procesada = preprocesar_texto(entrada_usuario)
    entrada_procesada_texto = " ".join(entrada_procesada)
    respuesta_generada = generar_texto(entrada_procesada_texto, max_length=100)
    return respuesta_generada


def chatgpt():
    while True:
        entrada_usuario = input("Usuario: ")
        
        if entrada_usuario.lower() == 'exit':
            print("Sistema: ¡Hasta luego!")
            break
        
        print(entrada_usuario)
    
        respuesta_generada = procesar_entrada_respuesta(entrada_usuario)
        
        respuesta = traductorES(respuesta_generada)

        pregunta = traductorEN(entrada_usuario)
        print(pregunta)
        
        print("Sistema:", respuesta)
