from django.urls import path
from a_customer import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-countries/', views.all_country_view, name='all_country_view'),
    path('search-country-for-name/', views.country_for_name_view, name='country_for_name_view'),
    path('guess-the-country/', views.random_country_view, name='random_country_view'),
    path('compare-countries', views.compare_countries_view, name='compare_countries_view'),
]