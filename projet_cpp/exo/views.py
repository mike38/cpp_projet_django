from django.shortcuts import render
from .models import Exercice, Chapitre, Fichier, Utilisation
from django.views import generic
from django.shortcuts import get_object_or_404
from datetime import date
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from .forms import FichierForm
from django.http import HttpResponseRedirect


def home(request):
    return render(request, 'exo/home.html', {})

class ExerciceListView(generic.ListView):
    model = Exercice
    paginate_by = 10

def detail(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    return render(request, 'exo/detail.html', {'exercice': exercice,
    	'fichiers': Fichier.objects.filter(exercice_id=exercice_id)},)


def search_chap(request):
	#exercice = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_chap', ''))
	#return render_to_response('')
	if request.method =="POST":
		searched = request.POST.get('searched')
		return render(request, 'exo/search_chap.html', {'searched' : searched})
	return render(request, 'exo/search_chap.html')


def upload_fichier(request,):
	if request.method == "POST":
		form = FichierForm(request.POST , request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/exercices/')
	else:
		form = FichierForm()
	return render(request, 'exo/up_fichier.html', {'form': form,})
