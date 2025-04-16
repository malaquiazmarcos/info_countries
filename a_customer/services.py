import requests
import json
import os

API_URL = 'https://restcountries.com/v3.1'

def get_all_countries():
    """
    Retrieve data for all countries from the REST Countries API.

    Workflow:
    1. Call the API whit relevant data for quick response. 
    2. Save the data in JSON file.
    3. In case of API error, search data in JSON file.

    Returns:
        - list: A list of dictionaries, containing country data.
                Retunrs an empty list in case of error.
    """
    try:
        response = requests.get(f'{API_URL}/all?fields=name,flags,capital,area,population,borders,continents,currencies,languages,maps,translations,latlng,region,subregion,timezones,independent,landlocked', timeout=15) 
        response.raise_for_status()  
        data = response.json()

        update_data = []

        for country in data:
            if country['name']['common'] != 'Falkland Islands':
                update_data.append(country)

        if update_data:
            with open('a_customer/data/country_data.json', 'w', encoding='utf-8') as f:
                json.dump(update_data, f, ensure_ascii=False, indent=4)

            return update_data
    
    except requests.exceptions.RequestException as e:
        print(f'Error when obtaining the countries: {e}')

        try:
            with open('a_customer/data/country_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileExistsError:
            print("Not local files")
            return []


        return []
    
def get_country_name(name_country):
    """
    Retrieve data for a specific country by name.

    Workflow:
    1. Call the API data. 
    2. Save the data in JSON file.
    3. In case of API error, search data in JSON file.

    Args:
        - name_country (str): The name of the country to search for.

    Returns:
        - dict: A dictionary containing the country data.
                Returns None in case of error.
    """

    cache_file = 'a_customer/data/search_data.json'

    try:

        if os.path.exists(cache_file):
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
        else:
            cache_data = []

        for country in cache_data:
            if country['name']['common'].lower() == name_country.lower():
                return [country]
        
        response = requests.get(f'{API_URL}/name/{name_country}?fullText=true', timeout=15)
        response.raise_for_status()
        data = response.json()

        if data:
            cache_data.append(data[0])

            with open('a_customer/data/search_data.json', 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=4)

            return data
    
    except requests.exceptions.RequestException as e:
        print(f'Error when obtaining the country: {e}')

        try:
            with open('a_customer/data/search_data.json', 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            for country in cache_data:
                if country['name']['common'].lower() == name_country.lower():
                    return [country]
            

        except FileExistsError:
            print("Not local files")
            return []
    
    """ try:
        response = requests.get(f'{API_URL}/name/{name_country}?fullText=true', timeout=15)
        response.raise_for_status()
        data = response.json()

        if data:
            with open('a_customer/data/search_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            return data

    except requests.exceptions.RequestException as e:
        print(f'Error when obtaining the country: {e}')

        try:
            with open('a_customer/data/search_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileExistsError:
            print("Not local files")
            return [] """

