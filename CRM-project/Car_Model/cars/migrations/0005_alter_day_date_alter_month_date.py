# Generated by Django 4.0.4 on 2022-04-13 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0004_alter_day_date_alter_month_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='day',
            name='date',
            field=models.DateTimeField(unique=True),
        ),
        migrations.AlterField(
            model_name='month',
            name='date',
            field=models.DateTimeField(unique=True),
        ),
    ]
