from django.urls import path
from a_customer import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todos-los-paises/', views.all_country_view, name='all_country_view'),
    path('buscar-pais-por-nombre/', views.country_for_name_view, name='country_for_name_view'),
]