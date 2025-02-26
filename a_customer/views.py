from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from a_customer.services import get_all_countries, get_country_name
from a_customer.forms import SearchCountry, GuessCountry, CompareCountries
from a_customer. utils import order_countries, order_countries_with_break, haversine
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
    latlng1, latlng2 = [], []
    not_found_1, not_found_2 = False, False
    distance = None
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
                for dicc in list_1:
                    latlng1 = dicc['latlng']
            else:
                not_found_1 = True
            if data_2:
                list_2 = order_countries_with_break(data_2)
                for dicc in list_2:
                    latlng2 = dicc['latlng']
            else:
                not_found_2 = True

            if latlng1 and latlng2:
                distance = haversine(latlng1[0], latlng1[1], latlng2[0], latlng2[1])
                distance = round(distance, 2)

    return render(request, 'paises/compare_countries.html', {
        'form':form,
        'list_1':list_1,
        'list_2':list_2,
        'name_1':name_1,
        'name_2':name_2, 
        'not_found_1':not_found_1,
        'not_found_2':not_found_2,
        'distance':distance
    })

def random_country_view(request):
    #random_country = None
    countries = get_all_countries()
    list_countries = order_countries(countries)

    random_country = request.session.get('random_country', None)
    print(random_country['name'])

    

    if request.method == 'POST':
        user_guess = request.POST.get('country-input', '').strip().lower()
        correct_name = random_country['name'].strip().lower()

        action = request.POST.get('action')

        print(f'this is the action: {action}')

        if action == 'refresh':
            print(f'this is the action: {action}')
            random_country = random.choice(list_countries)

            request.session['random_country'] = random_country
            request.session['random_country_name'] = random_country['name']
            

        print(f' this send the user: {user_guess} and this is the correct answer: {correct_name}')

        if user_guess == correct_name:
            return JsonResponse({'correct':True})
        else:
            return JsonResponse({'correct':False, 'correct_answer':correct_name})
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        random_country = random.choice(list_countries)

        request.session['random_country'] = random_country
        request.session['random_country_name'] = random_country['name']

        return JsonResponse({
            'name' : random_country['name'],
            'flags': random_country['flags']
        })

    return render(request, 'paises/pais_random.html', { 
        'list_coutries':list_countries,
        'random_country':random_country
    })