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
        fields = ['date']

        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
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
        fields = ['date']

        widgets = {
            'date': forms.DateTimeInput(attrs={'class': 'form-control'}),
        }

    def clean_slug(self):
        """May be needs rewriting"""

        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError("Slug may not be 'create'")
        if Month.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Slug must be unique. We have "{}"" slug already'.format(new_slug))

        return new_slug
