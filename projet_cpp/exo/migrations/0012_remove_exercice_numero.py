# Generated by Django 3.2 on 2021-05-29 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0011_auto_20210528_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercice',
            name='numero',
        ),
    ]
