from django.conf import settings
from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.urls import reverse


MATIERES = [('Maths', 'Maths'),('Chimie','Chimie'),
        ('Physique', 'Physique')]


class Chapitre(models.Model):
    annee = models.CharField(max_length=2, choices = [('1A', 'Première année'),
        ('2A', 'Deuxième année')])
    matiere = models.CharField(max_length=40 , choices = MATIERES)
    nom = models.CharField(max_length=200, null=False)
    numero = models.IntegerField(null=True, help_text="Vous pouvez numéroter le chapitre/module \
        pour permettre un classement dans l'ordre du programme (recommandé, \
        la valeur par défaut est 1)", default=1)

    def __str__(self):
        return self.nom #+ ' (' + self.matiere + ')'

    def get_absolute_url(self):
        return reverse('chapitre-details', args=[str(self.id)])


class Exercice(models.Model):
    nom = models.CharField(max_length=200, null=False)
    tags = TaggableManager()
    difficulte = models.IntegerField(null=True, choices = (('1', '*'), ('2', '**'),
        ('3', '***')))
    chapitre = models.ForeignKey(Chapitre, on_delete = models.CASCADE)

    def get_absolute_url(self):
        return reverse('exercice-details', args=[str(self.id)])

    def __str__(self):
        return self.nom + ' (' + self.chapitre.nom + ')'


class Fichier(models.Model):
    file = models.FileField(upload_to='')
    format = models.CharField(max_length = 2, choices = [('w', 'Document Word'),
        ('p', 'PDF'), ('t', 'LaTeX'), ('i', 'Image')])
    exercice = models.ForeignKey(Exercice, related_name = 'fichier',
        on_delete = models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    correction = models.CharField(max_length=3, choices = [('Oui', 'Oui'), ('Non', 'Non')], default='Non')


    def __str__(self):
        return self.exercice.nom + ' (' + self.exercice.chapitre.matiere + \
            self.exercice.chapitre.annee + ' - ' + self.exercice.chapitre.nom + \
            ', ' + self.format + ')'



class Utilisation(models.Model):
    type = models.CharField(max_length = 200, null = False)
    exercice = models.ForeignKey(Exercice, related_name = 'utilisation',
        on_delete = models.CASCADE)
    fichier = models.ManyToManyField(Fichier, blank=True)
    correction = models.BooleanField()


    def __str__(self):
        return self.exercice.nom + ' (' + self.type + ',' + str(self.correction) + ')'


