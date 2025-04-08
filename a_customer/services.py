import requests

API_URL = 'https://restcountries.com/v3.1'

def get_all_countries():
    """
    Retrieve data for all countries from the REST Countries API.

    Returns:
        - list: A list of dictionaries, containing country data.
                Retunrs an empty list in case of error.
    """
    try:
        response = requests.get(f'{API_URL}/all?fields=name,flags,capital,area,population,borders,continents,currencies,languages,maps,translations,latlng,region,subregion,timezones,independent,landlocked', timeout=15)   # Timeout para evitar esperas infinitas
        response.raise_for_status()  # Lanza error si la respuesta es 4xx o 5xx

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error when obtaining the countries: {e}')

        return []
    
def get_country_name(name_country):
    """
    Retrieve data for a specific country by name.

    Args:
        - name_country (str): The name of the country to search for.

    Returns:
        - dict: A dictionary containing the country data.
                Returns None in case of error.
    """
    try:
        response = requests.get(f'{API_URL}/name/{name_country}', timeout=15, verify=False)
        response.raise_for_status()

        return response.json()
    except requests.exceptions.RequestException as e:
        print(f'Error when obtaining the country: {e}')

        return None