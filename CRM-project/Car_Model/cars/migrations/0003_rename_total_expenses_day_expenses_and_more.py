# Generated by Django 4.0.4 on 2022-04-13 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_day_month'),
    ]

    operations = [
        migrations.RenameField(
            model_name='day',
            old_name='total_expenses',
            new_name='expenses',
        ),
        migrations.RenameField(
            model_name='day',
            old_name='total_income',
            new_name='income',
        ),
    ]