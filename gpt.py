import openai

openai.api_key = "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"

def chatgpt(prompt):

    response = openai.Completion.create(
        engine="text-davinci-003",  
        prompt=prompt,
        temperature=0.1,  
        max_tokens=200  
    )

    respuesta = response.choices[0].text.strip()
    
    return respuesta
