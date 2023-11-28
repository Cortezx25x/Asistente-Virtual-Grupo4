from googletrans import Translator


def traductorES(texto):    
    text = texto
    translator = Translator() 

    print(translator.translate(text , dest = 'es').text)


def traductorEN(texto):    
    text = texto
    translator = Translator() 

    print(translator.translate(text , dest = 'en').text)
