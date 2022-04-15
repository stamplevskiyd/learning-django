import datetime

from django.db import models
from django.dispatch import receiver
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

    def get_absolute_url(self):
        return reverse('car_detail_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('car_edit_url', kwargs={'id': self.id})

    def recount(self):
        for month in self.month_set.all():
            month.total_income = 0
            month.total_expenses = 0
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

    def save(self, *args, **kwargs):
        """Saves day object, adds it to month.
        Can create new month if needed."""
        month = self.month
        if not month.day_set.filter(id=self.id):
            """Creating new day object."""
            super().save(*args, **kwargs)
            month.day_set.add(self)
            month.total_expenses += self.expenses
            month.total_income += self.income
        else:
            """Modifying already added day."""
            day = month.day_set.get(id=self.id)
            month.total_expenses += self.expenses - day.expenses
            month.total_income += self.income - day.income
            super().save(*args, **kwargs)
        month.save()

    def __str__(self):
        return '{}'.format(self.date)


class Amortization(models.Model):
    """Amortization class."""

    start_date = models.DateField()
    end_date = models.DateField()
    money = models.IntegerField(default=0)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, default=get_default_car)

    def get_absolute_url(self):
        return reverse('amortization_detail_url', kwargs={'id': self.id})

    #@receiver(sender=)
    def save(self, *args, **kwargs):
        """Saves amortization object, adds it to car."""

        super().save(*args, **kwargs)
