from django import forms
from .models import Chapitre, Exercice, Fichier, Utilisation
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class FichierForm(forms.ModelForm):
    class Meta:
        model = Fichier
        fields = ['file', 'format', 'exercice', 'correction' ]


class ExerciceForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = ['nom', 'chapitre', 'tags', 'difficulte', 'provenance']
        help_texts = {
        	'nom' : 'L\'exercice sera automatiquement numéroté, mais vous \
        		pouvez ajouter un titre.',
        	'chapitre'  : '(*)',
            'tags': '(*) Mots-clés séparés par des virgules: ex. maths, matrices...',
            'provenance': 'ex. Banque Oral CCINP MP 2019'
        }

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ['annee', 'matiere', 'nom', 'numero', ]
        help_texts = {
        	'annee' : '(*)',
        	'matiere' : '(*)',
        	'nom' : '(*)',
        }

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	def inp_mail(self): #devrait empêcher les adresses ext à l'INP (ne fontionne pas)
		adresse = self.cleaned_data['email']
		if 'grenoble-inp' not in adresse:
			raise forms.ValidationError("Utilisez votre adresse INP")
		return adresse

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

