from django.shortcuts import render
from .models import Exercice, Chapitre, Fichier, Utilisation
from django.views import generic
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'exo/home.html', {})

class ExerciceListView(generic.ListView):
    model = Exercice

def detail(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    return render(request, 'exo/detail.html', {'exercice': exercice, 'fichiers': Fichier.objects.filter(exercice_id=exercice_id)})

