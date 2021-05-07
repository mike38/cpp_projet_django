from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager


class Chapitre(models.Model):
    annee = models.CharField(max_length=2, choices = [('1A', 'Première année'),('2A', 'Deuxième année')])
    matiere = models.CharField(max_length=2, choices = [('M', 'Maths'),('C',
        'Chimie'), ('P', 'Physique')])
    nom = models.CharField(max_length=200, null=False)


class Exercice(models.Model):
    nom = models.CharField(max_length=200, null=False)
    tags = TaggableManager()
    chapitre = models.ForeignKey(Chapitre, on_delete = models.CASCADE)


class Fichier(models.Model):
    file = models.FileField(upload_to='uploads/')
    format = models.CharField(max_length = 2, choices = [('w', 'Document Word'),
        ('p', 'PDF'), ('t', 'LaTeX'), ('i', 'Image')])
    exercice = models.ForeignKey(Exercice, related_name = 'fichier',
        on_delete = models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def ajouter(self): #fonction qui permettra d'ajouter des exos
        self.published_date = timezone.now()
        self.save()

    #def supprimer(self): #fonction qui permettra de supprimer des exos


    #def __str__(self):
    #    return self.title


class Utilisation(models.Model):
    date = models.DateTimeField()
    type = models.CharField(max_length = 200, null = False)
    exercice = models.ForeignKey(Exercice, related_name = 'utilisation',
        on_delete = models.CASCADE)
    correction = models.BooleanField()
