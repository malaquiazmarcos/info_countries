from django import forms

class SearchCountry(forms.Form):
    country_name = forms.CharField(
        label='Enter the country', 
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter the Country',
            'class': 'form-control'
            })
        )

class GuessCountry(forms.Form):
    country_name = forms.CharField(
        label='Enter the country', 
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Enter the Country'})
        )

class CompareCountries(forms.Form):
    country_name_1 = forms.CharField(
        label='Enter first country', 
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter first Country'})
        )
    country_name_2 = forms.CharField(
        label='Enter seconds country', 
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter second Country'})
        )