from django import forms

class SearchCountry(forms.Form):
    country_name = forms.CharField(label='Enter the country', max_length=100)

class GuessCountry(forms.Form):
    country_name = forms.CharField(label='Enter the country', max_length=100)

class CompareCountries(forms.Form):
    country_name_1 = forms.CharField(label='Enter first country', max_length=50)
    country_name_2 = forms.CharField(label='Enter seconds country', max_length=50)