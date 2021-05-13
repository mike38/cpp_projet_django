from django.shortcuts import render, redirect
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
    paginate_by = 2

def detail(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    return render(request, 'exo/detail.html', {'exercice': exercice,
    	'fichiers': Fichier.objects.filter(exercice_id=exercice_id)},)

def all_1A(request):
	prem_list = Chapitre.objects.filter(annee='1A').order_by('matiere', 'nom')
	return render(request, 'exo/1A.html', {'prem_list' : prem_list})

def all_2A(request):
	deux_list = Chapitre.objects.filter(annee='2A').order_by('matiere', '-nom')
	mat_list = Chapitre.objects.filter(matiere__contains='')
	return render(request, 'exo/2A.html', {'deux_list' : deux_list})


def search_chap(request):
	#exercice = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_chap', ''))
	#return render_to_response('')
	if request.method =="POST":
		searched = request.POST.get('searched')
		chapitres = Chapitre.objects.filter(nom__contains=searched)
		return render(request, 'exo/search_chap.html', {'searched' : searched,
			'chapitres' : chapitres})
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


def supp_ex(requst, exercice_id):
	exercice = Exercice.objects.get(pk=exercice_id)
	exercice.delete()
	return redirect('/exercices/')
