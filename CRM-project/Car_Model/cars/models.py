from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from time import time


def gen_slug(s: str):
    """Generates unique slug for every object"""

    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


def get_month(date_time: str) -> str:
    """Returns month and year number from date_time field."""
    year, month, day = str(date_time).split('-')[:3]  # формат всегда одинаковый
    return year + '-' + month


class Car(models.Model):
    """Basic class for car model"""

    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    register_date = models.DateTimeField()
    income = models.IntegerField(unique=False, default=0)
    expenses = models.IntegerField(unique=False, default=0)
    work_days = models.ManyToManyField('Day', blank=True, related_name='work_days')
    months = models.ManyToManyField('Month', blank=True, related_name='work_months')

    def get_absolute_url(self):
        return reverse('car_detail_url', kwargs={'slug': self.slug})

    def add_day(self, day):
        self.work_days.add(day)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)


class Day(models.Model):
    """Day class."""

    slug = models.SlugField(max_length=150, blank=True, unique=True)
    date = models.DateTimeField(unique=True)  # оставим пока без auto_now_date
    income = models.IntegerField(default=0)
    expenses = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('day_detail_url', kwargs={'slug': self.slug})

    def count_money(self):
        """Counts money earned by every car this day."""

        cars = Car.objects.filter(register_date__gte=self.date)
        for car in cars:
            days = car.work_days.all()
            if self in days:
                today_car = car.work_days.get(date__iexact=self.date)
                self.expenses += today_car.expenses
                self.income += today_car.income


    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.date)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.date)


class Month(models.Model):
    """Month class."""

    slug = models.SlugField(max_length=150, blank=True, unique=True)
    date = models.DateTimeField(unique=True)
    total_income = models.IntegerField(default=0)
    total_expenses = models.IntegerField(default=0)
    days = models.ManyToManyField('Day', blank=True, related_name='days')

    def get_absolute_url(self):
        return reverse('month_detail_url', kwargs={'slug': self.slug})

    def create_day(self, date_time):
        """Create new day in this month."""

        if get_month(date_time) != get_month(self.date):
            raise ValidationError("This day does not belong to this month")
        self.days.create(slug=gen_slug(str(date_time)), date=date_time,
                         income=0, expenses=0)

    def count_money(self):
        """Sums all expenses and income from every day in this month."""

        for day in self.days.all():
            self.total_expenses += day.expenses
            self.total_income += day.income

    def save(self, *args, **kwargs):
        """Save object."""

        if not self.id:
            self.slug = gen_slug(self.date)
        super().save(*args, **kwargs)
