from django.shortcuts import render, redirect
from .models import Exercice, Chapitre, Fichier, Utilisation, MATIERES
from django.views import generic
from django.shortcuts import get_object_or_404
from datetime import date
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from .forms import FichierForm, ExerciceForm, ChapitreForm, CreateUserForm
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, 'exo/home.html', {})

class ExerciceListView(generic.ListView):
    model = Exercice
    paginate_by = 4

def email_check(user):
    return user.email.endswith('@grenoble-inp.com' or '@grenoble-inp.org')

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Votre compte est créé ' + user + ' !')
				return redirect('login')
		context = {'form':form}
		return render(request, 'exo/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else :
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			if user is not None :
				login(request, user)
				return redirect('home')
			else :
				messages.info(request, 'Identifiant ou mot de passe erroné')
		context = {}
		return render(request, 'exo/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def detail(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    return render(request, 'exo/detail.html', {'exercice': exercice,
    	'fichiers': Fichier.objects.filter(exercice_id=exercice_id)},)

@login_required(login_url='login')
def all_1A(request):
	prem_list = Chapitre.objects.filter(annee='1A').order_by('matiere', 'numero')
	m_list = Chapitre.objects.filter(annee='1A').filter(matiere='Maths').order_by('numero')
	p_list = Chapitre.objects.filter(annee='1A', matiere='Physique').order_by('numero')
	c_list = Chapitre.objects.filter(annee='1A', matiere='Chimie').order_by('numero')
	return render(request, 'exo/1A.html', {'prem_list' : prem_list, 'm_list' : m_list,
		'p_list' : p_list, 'c_list' : c_list})

#@user_passes_test(email_check)
@login_required(login_url='login')
def maths_1A(request):
	m_list = Chapitre.objects.filter(annee='1A').filter(matiere='Maths').order_by('numero')
	return render(request, 'exo/1A-maths.html', {'m_list' : m_list})

@login_required(login_url='login')
def phys_1A(request):
	p_list = Chapitre.objects.filter(annee='1A', matiere='Physique').order_by('numero')
	return render(request, 'exo/1A-physique.html', {'p_list' : p_list})

@login_required(login_url='login')
def chim_1A(request):
	c_list = Chapitre.objects.filter(annee='1A', matiere='Chimie').order_by('numero')
	return render(request, 'exo/1A-chimie.html', {'c_list' : c_list})

@login_required(login_url='login')
def all_2A(request):
	deux_list = Chapitre.objects.filter(annee='2A').order_by('matiere', 'numero')
	m_list = Chapitre.objects.filter(annee='2A').filter(matiere='Maths').order_by('numero')
	p_list = Chapitre.objects.filter(annee='2A', matiere='Physique').order_by('numero')
	c_list = Chapitre.objects.filter(annee='2A', matiere='Chimie').order_by('numero')
	return render(request, 'exo/2A.html', {'deux_list' : deux_list, 'm_list' : m_list,
		'p_list' : p_list, 'c_list' : c_list})

@login_required(login_url='login')
def maths_2A(request):
	m_list = Chapitre.objects.filter(annee='2A').filter(matiere='Maths').order_by('numero')
	return render(request, 'exo/2A-maths.html', {'m_list' : m_list})

@login_required(login_url='login')
def phys_2A(request):
	p_list = Chapitre.objects.filter(annee='2A', matiere='Physique').order_by('numero')
	return render(request, 'exo/2A-physique.html', {'p_list' : p_list})

@login_required(login_url='login')
def chim_2A(request):
	c_list = Chapitre.objects.filter(annee='2A', matiere='Chimie').order_by('numero')
	return render(request, 'exo/2A-chimie.html', {'c_list' : c_list})

@login_required(login_url='login')
def search_chap(request):
	#exercice = SearchQuerySet().autocomplete(content_auto=request.POST.get('search_chap', ''))
	#return render_to_response('')
	if request.method =="POST":
		searched = request.POST.get('searched')
		chapitres = Chapitre.objects.filter(nom__contains=searched)
		exercices = Exercice.objects.filter(nom__contains=searched)
		return render(request, 'exo/search_chap.html', {'searched' : searched,
			'chapitres' : chapitres, 'exercices' : exercices})
	return render(request, 'exo/search_chap.html')


@login_required(login_url='login')
def upload_fichier(request):
	if request.method == "POST":
		form = FichierForm(request.POST , request.FILES)
		if form.is_valid():
			fichier = form.save(commit = False)
			fichier.save()
			return redirect('exercice-details', exercice_id = fichier.exercice.pk)
	else:
		form = FichierForm()
	return render(request, 'exo/up_fichier.html', {'form': form,})

@login_required(login_url='login')
def supp_ex(request, exercice_id):
	exercice = Exercice.objects.get(pk=exercice_id)
	exercice.delete()
	return redirect('/exercices/')

@login_required(login_url='login')
def add_ex(request):
	if request.method == "POST":
		form = ExerciceForm(request.POST)
		if form.is_valid():
			exercice = form.save(commit=False)
			exercice.save()
			return redirect('exercice-details', exercice_id = exercice.pk)
	else:
		form = ExerciceForm()
	return render(request, 'exo/new_ex.html', {'form': form,})

@login_required(login_url='login')
def add_chap(request):
	if request.method == "POST":
		form = ChapitreForm(request.POST)
		if form.is_valid():
			chapitre = form.save(commit = False)
			chapitre.save()
			return redirect('chapitre-details', chapitre_id = chapitre.pk)
	else:
		form = ChapitreForm()
	return render(request, 'exo/new_chap.html', {'form': form,})

@login_required(login_url='login')
def chap_detail(request, chapitre_id):
	chapitre = get_object_or_404(Chapitre, pk = chapitre_id)
	return render(request, 'exo/chap_listexo.html', {'chapitre': chapitre, 
	'exercices': Exercice.objects.filter(chapitre_id=chapitre_id),
	'fichiers' : Fichier.objects.all()})

class ChapitreListView(generic.ListView):
    model = Chapitre
    paginate_by = 4
    ordering = ['nom']

@login_required(login_url='login')
def exercice_edit(request, exercice_id):
	exercice = get_object_or_404(Exercice, pk=exercice_id)
	if request.method == "POST":
		form = ExerciceForm(request.POST, instance=exercice)
		if form.is_valid():
			exercice = form.save(commit=False)
			exercice.save()
			return redirect('exercice-details', exercice_id = exercice.pk)
	else:
		form = ExerciceForm(instance=exercice)
	return render(request, 'exo/edit_ex.html', {'form': form})
	