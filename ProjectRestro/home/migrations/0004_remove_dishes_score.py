# Generated by Django 3.1.6 on 2021-02-24 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_dishes_dish_view'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dishes',
            name='score',
        ),
    ]
