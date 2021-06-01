# Generated by Django 3.2 on 2021-06-01 12:23

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0015_alter_exercice_numero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fichier',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='fichier',
            name='published_date',
        ),
        migrations.AddField(
            model_name='fichier',
            name='date_modif',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
