import datetime

from django.db import models
from django.shortcuts import reverse
from django.core.exceptions import ValidationError
from time import time


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
    total_income = models.IntegerField(unique=False, default=0)
    total_expenses = models.IntegerField(unique=False, default=0)

    def get_absolute_url(self):
        return reverse('car_detail_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('car_edit_url', kwargs={'id': self.id})

    def recount(self):
        self.total_income = 0
        self.total_expenses = 0
        for month in self.month_set.all():
            month.total_income = 0
            month.total_expenses = 0
            for day in month.day_set.all():
                month.total_income += day.income
                month.total_expenses += day.expenses
            month.save()
            self.total_expenses += month.total_expenses
            self.total_income += month.total_income
        self.save()

    def __str__(self):
        return '{}'.format(self.title)


class Month(models.Model):
    """Month class."""

    date = models.DateField(unique=True)
    total_income = models.IntegerField(default=0)
    total_expenses = models.IntegerField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=get_default_car)

    def get_absolute_url(self):
        return reverse('month_detail_url', kwargs={'id': self.id})


class Day(models.Model):
    """Day class."""

    date = models.DateField(unique=True)
    income = models.IntegerField(default=0)
    expenses = models.IntegerField(default=0)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, default=get_default_month)

    def get_absolute_url(self):
        return reverse('day_detail_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('day_edit_url', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        """Saves day object, adds it to month.
        Can create new month if needed."""

        super().save(*args, **kwargs)
        month = Month.objects.get(date=datetime.date(self.date.year, self.date.month, 1))
        month.day_set.add(self)
        month.total_expenses += self.expenses
        month.total_income += self.income
        month.car.total_expenses += self.expenses
        month.car.total_income += self.income
        month.save()
        month.car.save()

    def __str__(self):
        return '{}'.format(self.date)
