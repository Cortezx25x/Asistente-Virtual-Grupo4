import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset, DataLoader
import numpy as np
import string
import unidecode

datos = [
    {"pregunta": "como estas", "respuesta": "Estoy bien, gracias."},
    {"pregunta": "¿Cuál es tu nombre?", "respuesta": "Soy un bot."},
    {"pregunta": "¿Qué te gusta hacer?", "respuesta": "Me gusta aprender y responder preguntas."},
    {"pregunta": "¿Cómo está el clima hoy?", "respuesta": "No estoy seguro, pero espero que esté soleado."},
    {"pregunta": "¿Qué día es hoy?", "respuesta": "Hoy es un gran día para aprender algo nuevo."},
    {"pregunta": "¿Cuál es tu color favorito?", "respuesta": "Me gustan todos los colores."},
    {"pregunta": "¿Qué te gusta hacer en tu tiempo libre?", "respuesta": "Me gusta leer y pasar tiempo al aire libre."},
    {"pregunta": "¿Cuál es tu comida favorita?", "respuesta": "Me encanta la comida italiana, especialmente la pizza."},
    {"pregunta": "¿Tienes alguna mascota?", "respuesta": "Sí, tengo un perro muy amigable."},
    {"pregunta": "¿Cuál es tu película favorita?", "respuesta": "Es difícil elegir, pero me encantan las películas de ciencia ficción."},
    {"pregunta": "¿Qué tipo de música te gusta?", "respuesta": "Disfruto de varios géneros, pero principalmente el rock y el pop."},
    {"pregunta": "¿Practicas algún deporte?", "respuesta": "Sí, me gusta correr y nadar."},
    {"pregunta": "¿Cuál es tu libro favorito?", "respuesta": "Hay muchos, pero 'El Principito' siempre tendrá un lugar especial en mi corazón."},
    {"pregunta": "¿Cuál es tu lugar favorito para vacacionar?", "respuesta": "Me encanta la playa, especialmente en verano."},
    {"pregunta": "¿Qué te gustaría aprender?", "respuesta": "Me gustaría aprender a tocar un instrumento musical, tal vez el piano."},
    {"pregunta": "¿Tienes algún hobby?", "respuesta": "Me gusta mucho la jardinería y la fotografía."},
    {"pregunta": "¿Cuál es tu estación del año favorita?", "respuesta": "Definitivamente la primavera, me encanta cuando todo florece."},
    {"pregunta": "¿Qué te hace feliz?", "respuesta": "Pasar tiempo con mi familia y amigos."},
    {"pregunta": "¿Cuál es tu serie de televisión favorita?", "respuesta": "Me gusta ver comedias, me ayudan a relajarme."},
    {"pregunta": "¿Qué idiomas hablas?", "respuesta": "Hablo español e inglés, y estoy aprendiendo francés."},
    {"pregunta": "¿Te gusta viajar?", "respuesta": "Sí, viajar es una de mis pasiones."},
    {"pregunta": "¿Cuál es tu animal favorito?", "respuesta": "Los delfines, son muy inteligentes y amigables."},
    {"pregunta": "¿Prefieres el café o el té?", "respuesta": "Definitivamente soy más de café."},
    {"pregunta": "¿Cuál es tu juego de mesa favorito?", "respuesta": "Me gusta jugar ajedrez, aunque no soy muy bueno."},
    {"pregunta": "¿Cuál es tu ciudad favorita?", "respuesta": "Me encanta París por su cultura y belleza."},
    {"pregunta": "¿Te gusta cocinar?", "respuesta": "Sí, especialmente probar recetas nuevas."},
    {"pregunta": "¿Cuál es tu postre favorito?", "respuesta": "No puedo resistirme a un buen pastel de chocolate."},
    {"pregunta": "¿Prefieres el campo o la ciudad?", "respuesta": "Disfruto de ambos, pero el campo tiene un encanto especial."},
    {"pregunta": "¿Cuál es tu flor favorita?", "respuesta": "Las rosas, son clásicas y bellas."},
    {"pregunta": "¿Cuál es tu superhéroe favorito?", "respuesta": "Spiderman, siempre me ha parecido un personaje interesante."},
    {"pregunta": "¿Cuál es tu videojuego favorito?", "respuesta": "Me gustan los juegos de aventuras y puzzles."},
    {"pregunta": "¿Cuál es tu bebida favorita?", "respuesta": "Un buen vaso de agua fresca siempre es lo mejor."},
    {"pregunta": "¿Prefieres los días soleados o lluviosos?", "respuesta": "Los días lluviosos tienen su encanto, son perfectos para leer un libro."}
]

vectorizer = CountVectorizer()
le = LabelEncoder()

preguntas = [d['pregunta'] for d in datos]
X = vectorizer.fit_transform(preguntas).toarray()
y = le.fit_transform([d['respuesta'] for d in datos])

class PreguntaRespuestaDataset(Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return torch.tensor(self.X[idx], dtype=torch.float32), torch.tensor(self.y[idx], dtype=torch.long)

dataset = PreguntaRespuestaDataset(X, y)
dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

class SimpleNN(nn.Module):
    def __init__(self, input_size, num_classes):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 50)
        self.fc2 = nn.Linear(50, num_classes)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

input_size = X.shape[1]
num_classes = len(le.classes_)
model = SimpleNN(input_size, num_classes)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

for epoch in range(100):
    for batch in dataloader:
        inputs, targets = batch
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

def normalizar_texto(texto):
    texto = texto.lower()  # Convertir a minúsculas
    texto = unidecode.unidecode(texto)  # Eliminar tildes
    texto = texto.translate(str.maketrans('', '', string.punctuation))  # Eliminar puntuación
    return texto

preguntas_normalizadas = [normalizar_texto(p) for p in preguntas]
X = vectorizer.fit_transform(preguntas_normalizadas).toarray()

def hacer_pregunta(pregunta):
    pregunta_normalizada = normalizar_texto(pregunta)
    input_vector = torch.tensor(vectorizer.transform([pregunta_normalizada]).toarray(), dtype=torch.float32)
    output = model(input_vector)

    probabilidad_maxima, predicted_idx = torch.max(output, 1)
    probabilidad_maxima = torch.softmax(output, dim=1)[0][predicted_idx.item()]
    umbral_confianza = 0.7

    if probabilidad_maxima.item() < umbral_confianza:
        return False
    else:
        respuesta_predicha = le.inverse_transform([predicted_idx.item()])[0]
        return respuesta_predicha


