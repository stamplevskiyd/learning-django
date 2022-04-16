from django.db import models
from django.db.models.signals import post_save, post_delete
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

    def total_recount(self):
        for month in self.month_set.all():
            month.total_income = 0
            month.total_expenses = 0
            month.total_amortization = 0
            month.total_profit = 0
            for day in month.day_set.all():
                day.amortization = 0
                day.profit = 0
                for am in self.amortization_set.all():
                    day_count = 0
                    for m in self.month_set.all():
                        day_count += m.day_set.filter(date__gte=am.start_date, date__lt=am.end_date).count()
                    if am.start_date <= day.date < am.end_date:
                        day.amortization += am.money // day_count
                day.profit = day.income - day.expenses - day.amortization
                day.save()
                month.total_income += day.income
                month.total_expenses += day.expenses
                month.total_amortization += day.amortization
            month.total_profit = month.total_income - month.total_expenses - month.total_amortization
            month.save()

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

    def recount(self):
        self.total_amortization = 0
        self.total_income = 0
        self.total_profit = 0
        self.total_expenses = 0
        for day in self.day_set.all():
            self.total_income += day.income
            self.total_expenses += day.expenses
            self.total_amortization += day.amortization
        self.total_profit = self.total_income - self.total_expenses - self.total_amortization
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
    month.recount()


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


@receiver(post_save, sender=Amortization)
def add_amortization(sender, instance, **kwargs):
    if instance.car_id == get_default_car():
        return
    day_count = (instance.end_date - instance.start_date).days
    money_per_day = instance.money // day_count
    for month in instance.car.month_set.all():
        for day in month.day_set.filter(date__gte=instance.start_date, date__lt=instance.end_date):
            day.amortization += money_per_day
            day.profit = day.income - day.expenses - day.amortization
            day.save()


@receiver(post_delete, sender=Amortization)
def delete_amortization(sender, instance, **kwargs):
    if instance.car_id == get_default_car():
        return
    day_count = (instance.end_date - instance.start_date).days
    money_per_day = instance.money // day_count
    for month in instance.car.month_set.all():
        for day in month.day_set.filter(date__gte=instance.start_date, date__lt=instance.end_date):
            day.amortization -= money_per_day
            day.profit += day.amortization
            day.save()
            print(day.amortization)
