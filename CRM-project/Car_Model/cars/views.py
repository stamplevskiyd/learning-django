from django.shortcuts import render
from django.views.generic import View

from .models import *
from .utils import *
from .forms import *


def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_index.html', context={'cars': cars})


def days_list(request):
    days = Day.objects.all()
    return render(request, 'cars/day_index.html', context={'days': days})


def months_list(request):
    months = Month.objects.all()
    return render(request, 'cars/month_index.html', context={'months': months})


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


class CarEdit(ObjectEditMixin, View):
    model = Car
    model_form = CarForm
    template = 'cars/car_edit_form.html'


class DayEdit(ObjectEditMixin, View):
    model = Day
    model_form = DayEditForm
    template = 'cars/day_edit_form.html'

    def get(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template,
                      context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        initial_income = obj.total_income
        initial_expenses = obj.total_expenses
        new_income = int(request.POST['total_income'])
        new_expences = int(request.POST['total_expenses'])
        obj.month.total_income += (new_income - initial_income)
        obj.month.total_expenses += (new_expences - initial_expenses)
        print(new_expences, new_income)
        obj.month.save()
        obj.save()
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form,
                                                       self.model.__name__.lower(): obj})
