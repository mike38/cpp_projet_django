from django import forms
from .models import Chapitre, Exercice, Fichier, Utilisation

class FichierForm(forms.ModelForm):
    class Meta:
        model = Fichier
        fields = ['file', 'format', 'exercice', ]


class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['nom', 'tags', 'chapitre', ]

