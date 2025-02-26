import pycountry
from math import sin, cos, atan2, sqrt, radians

def haversine(lat1, long1, lat2, long2):
    R = 6371  # radius of the earth in km

    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])

    a = sin((lat2-lat1)/2)**2 + cos(lat1) * cos(lat2) * sin((long2-long1)/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    d = R * c
    
    return d  # return the distance in km

def code__languages(codes):
    list_codes = []

    for code in codes:
        language = pycountry.languages.get(alpha_3=code)
        if language:
            list_codes.append(language.name)
    
    return list_codes


def code_borders(codes):
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
    list_codes = []

    for code in codes:
        currencies = pycountry.currencies.get(alpha_3=code)
        if currencies:
            list_codes.append(currencies.name)
    
    return list_codes

def code_currencies_symbol(currencies):
    symbol = []

    if currencies:
        for currency in currencies.values():
            symbol.append(f'({currency['symbol']})')
    else:
        symbol.append('Information not available')

    return symbol

def order_countries(countries):
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
        languages = code__languages(country.get('languages', ['Language information not available']))
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
        languages = code__languages(country.get('languages', ['Language information not available']))
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
