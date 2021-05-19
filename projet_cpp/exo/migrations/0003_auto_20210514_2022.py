# Generated by Django 3.2 on 2021-05-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0002_auto_20210514_1836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapitre',
            name='numero',
            field=models.IntegerField(default=1, help_text="Vous pouvez numéroter le chapitre/module pour permettre         un classement dans l'ordre du programme (facultatif)", null=True),
        ),
        migrations.AlterField(
            model_name='fichier',
            name='format',
            field=models.CharField(choices=[('W', 'Document Word'), ('P', 'PDF'), ('T', 'LaTeX'), ('I', 'Image')], max_length=2),
        ),
    ]