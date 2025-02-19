from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from a_customer.services import get_all_countries, get_country_name
from a_customer.forms import SearchCountry, GuessCountry, CompareCountries
from a_customer. utils import order_countries, order_countries_with_break
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
    not_found = None
    form = SearchCountry()

    # this comes to all countries
    if request.method == 'GET':
        country_name_link = request.GET.get('name', '')
        if country_name_link:
            form = SearchCountry(initial={'country_name':country_name_link})
            data_country = get_country_name(country_name_link)
            if data_country:
                list_country = order_countries(data_country)

    # this if the user send input with the name of country
    elif request.method == 'POST':
        form = SearchCountry(request.POST)
        if form.is_valid():
            country_name = form.cleaned_data['country_name']
            data_country = get_country_name(country_name)
            if data_country:
                list_country = order_countries(data_country)
            else:
                not_found = True
            return HttpResponseRedirect(f'{request.path}?name={country_name}')  # this redirect url with name of the country

    return render(request, 'paises/pais_nombre.html', {
        'form':form,
        'list_country':list_country,
        'not_found':not_found
    })

def compare_countries_view(request):
    list_1, list_2 = [], []
    name_1, name_2 = None, None
    not_found_1, not_found_2 = False, False
    form = CompareCountries()

    if request.method == 'POST':
        form = CompareCountries(request.POST)
        if form.is_valid():
            name_1 = form.cleaned_data['country_name_1']
            name_2 = form.cleaned_data['country_name_2']

            data_1 = get_country_name(name_1)
            data_2 = get_country_name(name_2)

            if data_1: 
                list_1 = order_countries_with_break(data_1)
            else:
                not_found_1 = True
            if data_2:
                list_2 = order_countries_with_break(data_2)
            else:
                not_found_2 = True
            
    return render(request, 'paises/compare_countries.html', {
        'form':form,
        'list_1':list_1,
        'list_2':list_2,
        'name_1':name_1,
        'name_2':name_2, 
        'not_found_1':not_found_1,
        'not_found_2':not_found_2
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