import django_filters
from .models import *

class ExerciceFilter(django_filters.FilterSet):
    class Meta:
        model = Exercice
        fields = {
            'nom': ['icontains'],
            'difficulte': ['exact'],
            'chapitre': ['exact'],
            'tags__name': ['icontains']
        }
        