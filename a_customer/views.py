from django.shortcuts import render, redirect
from a_customer.services import get_all_countries, get_country_name
from a_customer.forms import SearchCountry

def index(request):

    return render(request, 'base.html')

def all_country_view(request):
    countries = get_all_countries()

    list_countries = []

    for country in countries:
        name = country['name']['common']
        capital = country.get('capital', 'X')[0]
        flags = country['flags']['png']
        
        dicc_countries = {
            'name':name,
            'capital':capital,
            'flags':flags
        }

        list_countries.append(dicc_countries)

    order_list_countries = sorted(list_countries, key= lambda x: x['name'])

    return render(request, 'paises/todos.html', {
        'countries':countries,
        'order_list_countries':order_list_countries,
    })

def country_for_name_view(request):
    list_country = []
    
    if request.method == 'POST':
        form = SearchCountry(request.POST)

        if form.is_valid():
            country_name = form.cleaned_data['country_name']

            data_country = get_country_name(country_name)

            for data in data_country:
                name = data['name']['common']
                capital = data.get('capital', 'X')[0]
                flags = data['flags']['png']

                dicc_countries = {
                    'name':name,
                    'capital':capital,
                    'flags':flags
                }

                list_country.append(dicc_countries)

    else:
        form = SearchCountry()

    return render(request, 'paises/pais_nombre.html', {
        'form':form,
        'list_country':list_country
    })
