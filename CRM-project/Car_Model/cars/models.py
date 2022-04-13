from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from time import time


def gen_slug(s: str):
    """Generates unique slug for every object"""

    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Car(models.Model):
    """Basic class for car model"""

    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    register_date = models.DateTimeField(auto_now_add=True)
    #income = models.IntegerField(unique=False)
    #expenses = models.IntegerField(unique=False)
    #days = models.ManyToManyField('Day', blank=True, related_name='days')
    #months = models.ManyToManyField('Month', blank=True, related_name='months')

    def get_absolute_url(self):
        return reverse('car_detail_url', kwargs={'slug': self.slug})

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

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.date)
        super().save(*args, **kwargs)


class Month(models.Model):
    """Month class."""

    slug = models.SlugField(max_length=150, blank=True, unique=True)
    date = models.DateTimeField(unique=True)  # оставим пока без auto_now_date
    total_income = models.IntegerField(default=0)
    total_expenses = models.IntegerField(default=0)
    days = models.ManyToManyField('Day', blank=True, related_name='days')

    def get_absolute_url(self):
        return reverse('month_detail_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.date)
        super().save(*args, **kwargs)
