from django.shortcuts import render
from .models import Exercice, Chapitre, Fichier, Utilisation
from django.views import generic

def home(request):
    return render(request, 'exo/home.html', {})

class ExerciceListView(generic.ListView):
    model = Exercice

class ExerciceDetailView(generic.DetailView):
    model = Exercice