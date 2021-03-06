# Generated by Django 3.2.2 on 2021-05-17 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisation',
            name='date',
        ),
        migrations.AddField(
            model_name='chapitre',
            name='numero',
            field=models.IntegerField(default=1, help_text="Vous pouvez numéroter le chapitre/module         pour permettre un classement dans l'ordre du programme (recommandé,         la valeur par défaut est 1)", null=True),
        ),
        migrations.AddField(
            model_name='utilisation',
            name='fichier',
            field=models.ManyToManyField(blank=True, to='exo.Fichier'),
        ),
        migrations.AlterField(
            model_name='chapitre',
            name='matiere',
            field=models.CharField(choices=[('Maths', 'Maths'), ('Chimie', 'Chimie'), ('Physique', 'Physique')], max_length=40),
        ),
        migrations.AlterField(
            model_name='fichier',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]
