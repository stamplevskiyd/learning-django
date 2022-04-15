from django import forms
from .models import *
from django.core.exceptions import ValidationError


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'register_date']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'register_date': forms.TextInput(attrs={'class': 'form-control'})
        }


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['date', 'income', 'expenses']

        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'income': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'expenses': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }


class DayEditForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['income', 'expenses']

        widgets = {
            'income': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'expenses': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }


class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = ['date']

        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }


class AmortizationForm(forms.ModelForm):
    class Meta:
        model = Amortization
        fields = ['start_date', 'end_date', 'money']

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'end_day': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'money': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }
