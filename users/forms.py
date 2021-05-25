# Importing Forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account 

YEARS = [x for x in range(1950, 2021)]
CHOICES = [('1', 'Male'), ('2', 'Female'), ('3', 'Other')] 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    dob = forms.DateField(label="Date of Birth", initial='1999-06-10', widget=forms.SelectDateWidget(years=YEARS))
    gender = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = Account
        fields = ("username", "email", "gender", "dob", "password1", "password2")
