from django import forms

class SearchCountry(forms.Form):
    country_name = forms.CharField(label='Enter the country', max_length=100)