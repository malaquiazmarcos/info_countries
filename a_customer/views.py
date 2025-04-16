from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from a_customer.services import get_all_countries, get_country_name
from a_customer.forms import SearchCountry, CompareCountries
from a_customer. utils import order_countries, order_countries_with_break, haversine
import random

def index(request):
    """
    View to show the base template.
    """

    return render(request, 'base.html')

def all_country_view(request):
    """
    View to show all the countries.

    Steps:
    1. Call the API using 'get_all_countries()'
    2. Extract relevant data for the countries using 'order_countries(countries)'
    3. Sort by a-z name.
    """
    countries = get_all_countries()
    list_countries = order_countries(countries)

    order_list_countries = sorted(list_countries, key= lambda x: x['name']) 

    return render(request, 'paises/todos.html', {
        'countries':countries,
        'order_list_countries':order_list_countries,
    })

def country_for_name_view(request):
    """
    View allows to search any country.

    Workflow:
    1. Initialize an empty form and country list.
    2. If 'not_found = None' the template it's going well.
    3. Handle Get request, the name comes from URL:
        - Get the name from URL.
        - Put an initial data in form and call the API with the country name. 
        - Extract relevant data from the countries.
    4. Handle POST request, the name comes to the imput from user send:
        - Proccess the form and obtain the name of the country.
        - Fetch the API with the name and extract relevant data in list
        - If 'not_found = True' the template show an exeption.
    """
    list_country = []
    not_found = None
    country_name = None
    form = SearchCountry()

    # Search by URL parameter
    if request.method == 'GET':
        country_name_link = request.GET.get('name', '')
        if country_name_link:
            form = SearchCountry(initial={'country_name':country_name_link})
            data_country = get_country_name(country_name_link)
            if data_country:
                list_country = order_countries(data_country)

    # Search by user input
    elif request.method == 'POST':
        form = SearchCountry(request.POST)
        if form.is_valid():
            country_name = form.cleaned_data['country_name']
            data_country = get_country_name(country_name)
            if data_country:
                list_country = order_countries(data_country)

                # Redirect to the URL with the country name as a query parameter
                return HttpResponseRedirect(f'{request.path}?name={country_name}')
            else:
                print('here a error')
                not_found = True     

    return render(request, 'paises/pais_nombre.html', {
        'form':form,
        'list_country':list_country,
        'not_found':not_found,
        'country_name':country_name
    })

def compare_countries_view(request):
    """
    View that compare two countries.

    Workflow:
    1. Initialize lists, variables and the form.
    2. Handle POST request:
        - Get data from input the forms.
        - Fetch country data from the API.
        - If data is found, obtain the lat and long.
        - If not data, send a signal to template for handle a exeption.
        - Calculate the distance if exists lat and long.
    """
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
    """
    View for select a random country.

    In this view, occupate AJAX for asyncronic task
    of this way not reload the pages. 

    Workflow:
    1. Fetch all countries from the API and extract the independent.
    2. Extract the relevant data.
    3. If not country in session, obtain a random and save a new one.
    4. Handle POST request:
        - Get random country in session, user input and correct answer.
        - Handle if answer is correct or not.
    5. Handle if request comes to AJAX:
        - If not list with countries and not random country returns an exeption.
        - Select a random country and save in session.    
    """
    countries = get_all_countries()
    list_countries_ni = [x for x in countries if x.get('independent', False) != False]

    list_countries = order_countries(list_countries_ni)

    random_country = None                      

    if 'random_country' not in request.session:
        request.session['random_country'] = random.choice(list_countries)
        request.session['random_country_name'] = request.session['random_country']['name']

    if request.method == 'POST':
        random_country = request.session.get('random_country', None)
        user_guess = request.POST.get('country-input', '').strip().lower()
        correct_name = random_country['name'].strip().lower()

        if user_guess == correct_name:
            return JsonResponse({'correct':True, 'correct_answer':correct_name})
        else:
            return JsonResponse({'correct':False, 'correct_answer':correct_name})
        
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try: 
            if not list_countries:
                return JsonResponse({'error': 'No countries available'}, status=404)

            random_country = random.choice(list_countries)

            if not random_country:
                return JsonResponse({'error': 'Failed to select a country'}, status=500)

            request.session['random_country'] = random_country
            request.session['random_country_name'] = random_country['name']

            return JsonResponse({
                'name' : random_country['name'],
                'flags': random_country['flags']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'paises/pais_random.html', { 
        'list_coutries':list_countries,
        'random_country':random_country
    })