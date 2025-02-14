import requests

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