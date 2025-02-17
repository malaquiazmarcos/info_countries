from django.shortcuts import render, redirect
from a_customer.services import get_all_countries, get_country_name
from a_customer.forms import SearchCountry, GuessCountry
from a_customer. utils import order_countries
import random

def index(request):

    return render(request, 'base.html')

def all_country_view(request):
    countries = get_all_countries()
    list_countries = order_countries(countries)

    order_list_countries = sorted(list_countries, key= lambda x: x['name'])  # ordena por nombre

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
            if data_country:
                list_country = order_countries(data_country)
            else:
                print('The conuntry was not found')
            #print(data_country)

    else:
        form = SearchCountry()

    return render(request, 'paises/pais_nombre.html', {
        'form':form,
        'list_country':list_country
    })

def random_country_view(request):
    countries = get_all_countries()
    list_countries = order_countries(countries)

    random_country = random.choice(list_countries)

    country_name = None

    if request.method == 'POST':    
        form = GuessCountry(request.POST)

        if form.is_valid():
            country_name = form.cleaned_data['country_name']

    else:
        form = GuessCountry()


    return render(request, 'paises/pais_random.html', {
        'form':form, 
        'list_coutries':list_countries,
        'random_country':random_country
    })
