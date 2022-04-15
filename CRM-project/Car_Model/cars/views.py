from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.views.generic import View

from .models import *
from .forms import *


def create_month(date: str):
    """Creates month record from standard date"""

    year, month, day = date.split('-')[:3]
    return year + '-' + month + '-01'


def cars_list(request):
    cars = Car.objects.all()
    return render(request, 'cars/car_index.html', context={'cars': cars})


def days_list(request):
    days = Day.objects.all()
    return render(request, 'cars/day_index.html', context={'days': days})


def months_list(request):
    months = Month.objects.all()
    return render(request, 'cars/month_index.html', context={'months': months})


class CarDetail(View):
    template = 'cars/car_detail.html'

    def get(self, request, id):
        obj = get_object_or_404(Car, id=id)
        return render(request, self.template, context={'car': obj})


class DayDetail(View):
    template = 'cars/day_detail.html'

    def get(self, request, id):
        obj = get_object_or_404(Day, id=id)
        return render(request, self.template, context={'day': obj})


class MonthDetail(View):
    template = 'cars/month_detail.html'

    def get(self, request, id):
        obj = get_object_or_404(Month, id=id)
        return render(request, self.template, context={'month': obj})


class CarCreate(View):
    template = 'cars/car_create_form.html'

    def get(self, request):
        form = CarForm()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = CarForm(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class DayCreate(View):
    """Adds day to required car"""

    template = 'cars/day_create_form.html'

    def get(self, request, id):
        form = DayForm()
        return render(request, self.template, context={'form': form, 'id': id})

    def post(self, request, id):
        car = Car.objects.get(id=id)
        date = request.POST['date']
        post_month = car.month_set.get_or_create(date=create_month(date))[0]
        bound_form = DayForm(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class MonthCreate(View):
    template = 'cars/month_create_form.html'

    def get(self, request):
        form = MonthForm()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = MonthForm(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class CarEdit(View):
    model = Car
    model_form = CarForm
    template = 'cars/car_edit_form.html'

    def get(self, request, id):
        obj = Car.objects.get(id=id)
        bound_form = CarForm(instance=obj)
        return render(request, self.template, context={'form': bound_form, 'car': obj})

    def post(self, request, id):
        obj = Car.objects.get(id=id)
        bound_form = CarForm(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, 'car': obj})


class DayEdit(View):
    template = 'cars/day_edit_form.html'

    def get(self, request, id):
        obj = Day.objects.get(id=id)
        bound_form = DayEditForm(instance=obj)
        return render(request, self.template,
                      context={'form': bound_form, 'day': obj})

    def post(self, request, id):
        obj = Day.objects.get(id=id)
        bound_form = DayEditForm(request.POST, instance=obj)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, 'day': obj})