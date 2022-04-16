from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from time import time
import datetime


def create_default_month():
    return Month.objects.get_or_create(date='2000-01-01')[0]


def get_default_month():
    return create_default_month().id


def create_default_car():
    return Car.objects.get_or_create(title='Default Car', register_date='2000-01-01')[0]


def get_default_car():
    return create_default_car().id


class Car(models.Model):
    """Basic class for car model"""

    title = models.CharField(max_length=100, db_index=True)
    register_date = models.DateField(blank=False)

    def get_absolute_url(self):
        return reverse('car_detail_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('car_edit_url', kwargs={'id': self.id})


    def recount(self):
        for month in self.month_set.all():
            month.total_income = 0
            month.total_expenses = 0
            month.total_amortization = 0
            month.total_profit = 0
            for day in month.day_set.all():
                day.save()

    def __str__(self):
        return '{}'.format(self.title)


class Month(models.Model):
    """Month class."""

    date = models.DateField(unique=False)
    total_income = models.IntegerField(default=0)
    total_expenses = models.IntegerField(default=0)
    total_amortization = models.IntegerField(default=0)
    total_profit = models.IntegerField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=get_default_car)

    def get_absolute_url(self):
        return reverse('month_detail_url', kwargs={'id': self.id})

    def add_day_data(self, day):
        self.total_income += day.income
        self.total_expenses += day.expenses
        self.save()


class Day(models.Model):
    """Day class."""

    date = models.DateField(unique=False)
    income = models.IntegerField(default=0)
    expenses = models.IntegerField(default=0)
    amortization = models.IntegerField(default=0)
    profit = models.IntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, default=get_default_month)

    def get_absolute_url(self):
        return reverse('day_detail_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('day_edit_url', kwargs={'id': self.id})

    def __str__(self):
        return '{}'.format(self.date)


@receiver(post_save, sender=Day)
def add_day_data(sender, instance, **kwargs):
    month = Month.objects.get(day__id=instance.id)  # они и так все уникальны
    if month == get_default_month():  # при создании шаблонного объекта случится дичь
        return
    month.add_day_data(instance)


class Amortization(models.Model):
    """Amortization class."""

    start_date = models.DateField()
    end_date = models.DateField()
    money = models.IntegerField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=get_default_car)

    def get_absolute_url(self):
        return reverse('amortization_detail_url', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('amortization_delete_url', kwargs={'id': self.id})
