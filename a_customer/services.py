import requests
from decouple import config

API_URL = 'https://restcountries.com/v3.1'

def get_all_countries():
    try:
        response = requests.get(f'{API_URL}/all', timeout=5)   # Timeout para evitar esperas infinitas
        response.raise_for_status()  # Lanza error si la respuesta es 4xx o 5xx

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener países: {e}')

        return []
    
def get_country_name(name_country):
    try:
        response = requests.get(f'{API_URL}/name/{name_country}', timeout=5)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error al obtener el país: {e}')


""" API_URL_GPTJ = "https://api-inference.huggingface.co/models/gpt2"
HEADERS = {'Authorization':f'Bearer {config('API_KEY_GPTJ')}'}

def query(text):
    try:
        payload = {
            'inputs':text,
            'parameters': {
                "max_length": 200,  # Ajusta la longitud
                "temperature": 0.7,  # Controla la aleatoriedad
                "top_p": 0.9  # Controla la diversidad de respuestas
            }}
        response = requests.post(API_URL_GPTJ, headers=HEADERS, json=payload)
        response.raise_for_status()
    
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f'Error: {e}') """