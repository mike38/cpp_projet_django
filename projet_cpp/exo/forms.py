from django import forms
from .models import Chapitre, Exercice, Fichier, Utilisation

class FichierForm(forms.ModelForm):
    class Meta:
        model = Fichier
        fields = ['file', 'format', 'exercice', 'correction' ]


class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['nom', 'tags', 'chapitre', ]

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ['annee', 'matiere', 'nom', 'numero', ]

