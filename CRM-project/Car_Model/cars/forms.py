from django import forms
from .models import *
from django.core.exceptions import ValidationError


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['title', 'slug']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        """May be needs rewriting"""

        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError("Slug may not be 'create'")
        if Car.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}"" slug already'.format(new_slug))

        return new_slug


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ['slug', 'date', 'income', 'expenses']

        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'income': forms.NumberInput(attrs={'class': 'form-control'}),
            'expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        """May be needs rewriting"""

        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError("Slug may not be 'create'")
        if Day.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}"" slug already'.format(new_slug))

        return new_slug


class MonthForm(forms.ModelForm):
    class Meta:
        model = Month
        fields = ['date', 'total_income', 'total_expenses', 'slug']

        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
            'total_income': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_expenses': forms.NumberInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'days': Day.objects.filter(date__month__iexact=1)  # фильтр по месяцу. Пока - заглушка
        }

    def clean_slug(self):
        """May be needs rewriting"""

        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError("Slug may not be 'create'")
        if Month.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}"" slug already'.format(new_slug))

        return new_slug
