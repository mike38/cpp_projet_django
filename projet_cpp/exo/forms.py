from django import forms
from .models import Chapitre, Exercice, Fichier, Utilisation

class FichierForm(forms.ModelForm):
    class Meta:
        model = Fichier
        fields = ['file', 'format', 'exercice', ]

