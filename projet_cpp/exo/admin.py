from django.contrib import admin

from .models import Exercice, Chapitre, Fichier, Utilisation

admin.site.register(Exercice)
admin.site.register(Chapitre)
admin.site.register(Fichier)
admin.site.register(Utilisation)
