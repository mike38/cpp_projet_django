from django import forms
from .models import Chapitre, Exercice, Fichier, Utilisation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class FichierForm(forms.ModelForm):
    class Meta:
        model = Fichier
        fields = ['file', 'format', 'exercice', 'correction' ]


class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['nom', 'tags', 'chapitre', 'difficulte']

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ['annee', 'matiere', 'nom', 'numero', ]

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

