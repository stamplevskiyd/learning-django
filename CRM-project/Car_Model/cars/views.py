from django.shortcuts import render
from django.views.generic import View


from .models import Car
from .utils import *
from .forms import CarForm, DayForm, MonthForm

def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_index.html', context={'cars': cars})

def days_list(request):
    days = Day.objects.all()
    return render(request, 'cars/day_index.html', context={'days': days})


class CarDetail(ObjectDetailMixin, View):
    model = Car
    template = 'cars/car_detail.html'


class DayDetail(ObjectDetailMixin, View):
    model = Day
    template = 'cars/day_detail.html'

class MonthDetail(ObjectDetailMixin, View):
    model = Month
    template = 'cars/month_detail.html'


class CarCreate(ObjectCreateMixin, View):
    form_model = CarForm
    template = 'cars/car_create_form.html'


class DayCreate(ObjectCreateMixin, View):
    form_model = DayForm
    template = 'cars/day_create_form.html'

class MonthCreate(ObjectCreateMixin, View):
    form_model = MonthForm
    template = 'cars/month_create_form.html'
