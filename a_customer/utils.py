import pycountry
from math import sin, cos, atan2, sqrt, radians

def haversine(lat1, long1, lat2, long2):
    """
    Calculates the distance between two countries 
    using the Haversine formula.

    Args: 
        - lat1 (float): Latitude on the first location.
        - long1 (float): Longitude on the first location.
        - lat2 (float): Latitude on the second location.
        - long2 (float): Longitude on the second location.

    returns:
        - d: distance in km.
    """
    R = 6371  # radius of the earth in km

    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

    a = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((long2-long1)/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    
    return d 

def code_languages(codes):
    """
    Convert ISO 639-3 alpha-3 codes into full language name.

    Args:
        - codes (list): containing codes ISO 639-3 (e.g. [spa, eng])

    Returns:
        - list_codes (list): the full language name or ['Unknown language'] if empty.
    """
    if not codes:
        return ['Unknown language']
    
    list_codes = []

    for code in codes:
        language = pycountry.languages.get(alpha_3=code)
        if language:
            list_codes.append(language.name)
    
    return list_codes


def code_borders(codes):
    """
    Convert ISO 3166-1 alpha-3 codes into full countries name.

    Args:
        - codes (list): containing codes ISO 3166-1 (e.g. [BRA, PAR, BOL, CHI] borders of Argentina).

    Returns:
        - list_codes (list): the complete name of the countries or ['No bordering countries'] if empty.
    """
    if not codes:
        return ['No bordering countries']

    list_codes = []

    for code in codes:
        country = pycountry.countries.get(alpha_3=code) 
        if country:
            country_name = getattr(country, 'common_name', country.name)
            list_codes.append(country_name) 

    return list_codes

def code_currencies(codes):
    """
    Convert ISO 4217 alpha-3 into full currencies name.

    Args: 
        - codes (list): Containing codes ISO 4217 (e.g. [ARS, EUR, USD]).

    Returns:
        - list_codes (list): the complete full currencies name or ['Unkown currencies'] if empty.
    """
    if not codes:
        return ['Unkown currencies']
    
    list_codes = []

    for code in codes:
        currencies = pycountry.currencies.get(alpha_3=code)
        if currencies:
            list_codes.append(currencies.name)
    
    return list_codes

def code_currencies_symbol(currencies):
    """
    Iterates about the dictionary and obtain the symbol of currency.

    Args:
        - currencies (dict): diccionary with currencies data (e.g.  {'currencies': {'TRY': {'name': 'Turkish lira', 'symbol': '₺'}}}).

    Returns:
        - symbol (list): all symbols of every country.
    """
    symbol = []

    if currencies:
        for currency in currencies.values():
            symbol.append(f"({currency['symbol']})")
    else:
        symbol.append('Information not available')

    return symbol

def order_countries(countries):
    """
    Extract the relevant data and fetch the REST Counties API.

    The API data first stored in a dictionay, after into a list.

    Args:
        - countries (list): this list containing many dictionaries with API data.

    Returns:
        - list_countries (list): other list, this containing only the relevant data.
    """
    list_countries = []

    for country in countries:
        name = country['name']['common']
        official_name = country['name']['official']
        capital = country.get('capital', ['No capital city'])
        area = country['area']
        population = country['population']
        borders = code_borders(country.get('borders', []))  
        continents = country['continents']
        currencies = code_currencies(country.get('currencies', ''))
        currencies_symbol = code_currencies_symbol(country.get('currencies'))
        languages = code_languages(country.get('languages', ['Language information not available']))
        maps = country['maps']
        demonyms = country.get('demonyms', {}).get('eng', {}).get('m', 'Information not available')
        translations = country['translations']['spa']['common']
        latlng = country['latlng']
        region = country['region']
        subregion = country.get('subregion','')
        timezones = country['timezones']
        independent = 'Yes' if country.get('independent', 'Information not available') else 'No'
        landlocked = 'No' if country['landlocked'] else 'Yes'
        flags = country['flags']['png']
        
        dicc_countries = {
            'name':name,
            'official_name':official_name,
            'capital':capital,
            'area':area,
            'population':population,
            'borders':borders,
            'continents':continents,
            'currencies':currencies,
            'currencies_symbol':currencies_symbol,
            'languages':languages,
            'maps':maps,
            'demonyms':demonyms,
            'translations':translations,
            'latlng':latlng,
            'region':region,
            'subregion':subregion,
            'timezones':timezones,
            'independent':independent,
            'landlocked':landlocked,
            'flags':flags
        }

        list_countries.append(dicc_countries)
    
    return list_countries

def order_countries_with_break(countries):
    """
    Extract the relevant data and fetch the REST Country API.

    This function is similar to the up, but only choose the first country that matches
    with the request of the user. Using in the view for search one country for name to avoid
    showing many countries (e.g. if search letter A: Argentina, Algeria, ...)

    Args:
        - countries (list): this list containing many dictionaries with API data.

    Returns:
        - list_countries (list): other list, this containing only the relevant data.
    """
    list_countries = []

    for country in countries:
        name = country['name']['common']
        official_name = country['name']['official']
        capital = country.get('capital', ['No capital city'])
        area = country['area']
        population = country['population']
        borders = code_borders(country.get('borders', []))  
        continents = country['continents']
        currencies = code_currencies(country.get('currencies', ''))
        currencies_symbol = code_currencies_symbol(country.get('currencies'))
        languages = code_languages(country.get('languages', ['Language information not available']))
        maps = country['maps']
        demonyms = country.get('demonyms', {}).get('eng', {}).get('m', 'Information not available')
        translations = country['translations']['spa']['common']
        latlng = country['latlng']
        region = country['region']
        subregion = country.get('subregion','')
        timezones = country['timezones']
        independent = 'Yes' if country.get('independent', 'Information not available') else 'No'
        landlocked = 'No' if country['landlocked'] else 'Yes'
        flags = country['flags']['png']
        
        dicc_countries = {
            'name':name,
            'official_name':official_name,
            'capital':capital,
            'area':area,
            'population':population,
            'borders':borders,
            'continents':continents,
            'currencies':currencies,
            'currencies_symbol':currencies_symbol,
            'languages':languages,
            'maps':maps,
            'demonyms':demonyms,
            'translations':translations,
            'latlng':latlng,
            'region':region,
            'subregion':subregion,
            'timezones':timezones,
            'independent':independent,
            'landlocked':landlocked,
            'flags':flags
        }

        list_countries.append(dicc_countries)

        break
    
    return list_countries
