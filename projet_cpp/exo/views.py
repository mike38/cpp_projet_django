from django.shortcuts import render, redirect
from .models import Exercice, Chapitre, Fichier, Utilisation, MATIERES
from django.views import generic
from django.shortcuts import get_object_or_404
from datetime import date
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .decorators import unauthenticated_user, allowed_users#, wrong_email
from django.contrib.auth.models import Group, User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import send_mail, EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.urls import reverse_lazy, reverse
from django.views.generic import View, UpdateView
from django.contrib.auth.models import User
from .utils import token_generator
from .filters import ExerciceFilter
from django.core.paginator import Paginator

def home(request):
    return render(request, 'exo/home.html', {})

def acces_interdit(request):
	return render(request, 'exo/acces_interdit.html', {})

class ExerciceListView(generic.ListView):
    model = Exercice
    paginate_by = 10

def email_check(user):
    return user.email.endswith('@grenoble-inp.org') or user.email.endswith('@grenoble-inp.fr')


@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(request, 'Veuillez confirmer votre email pour compléter la création de votre compte')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            current_site = get_current_site(request)
            mail_subject = 'Activez votre compte sur ExoCpp'
            message = render_to_string('exo/acc_active_email.html', {'user': user,'domain': current_site.domain,
            	'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            	'token':account_activation_token.make_token(user),})
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            if list(to_email)[-1] == 'g': #pour les élèves
            	group = Group.objects.get(name='etudiant')
            	user.groups.add(group)
			# elif list(to_email)[-1] == 'r': #pour les profs (ne fonctionne pas)
   #          	group = Group.objects.get(name='prof')
   #          	user.groups.add(group)
            # messages.success(request, f'Votre compte a bien été créé ! Vous pouvez dès à présent vous connecter.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'exo/register.html', {'form': form, 'title':'register here'})
  
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, ('Votre compte est maintenant créé.'))
        return redirect('home')
    else:
        return HttpResponse('Lien d\'activation invalide !')


@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None :
			form = login(request, user)
			messages.success(request, 'Votre compte est créé ' + username + ' !')
			return redirect('home')
		else :
			messages.info(request, 'Identifiant ou mot de passe erroné')
	form = AuthenticationForm()
	return render(request, 'exo/login.html', {'form':form, 'title':'log in'})

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def detail(request, exercice_id):
    exercice = get_object_or_404(Exercice, pk=exercice_id)
    return render(request, 'exo/detail.html', {'exercice': exercice,
    	'fichiers': Fichier.objects.filter(exercice_id=exercice_id),
		'utilisations': Utilisation.objects.filter(exercice_id=exercice_id)},)

@login_required(login_url='login')
def all_1A(request):
	prem_list = Chapitre.objects.filter(annee='1A').order_by('matiere', 'numero')
	m_list = Chapitre.objects.filter(annee='1A').filter(matiere='Maths').order_by('numero')
	p_list = Chapitre.objects.filter(annee='1A', matiere='Physique').order_by('numero')
	c_list = Chapitre.objects.filter(annee='1A', matiere='Chimie').order_by('numero')
	return render(request, 'exo/1A.html', {'prem_list' : prem_list, 'm_list' : m_list,
		'p_list' : p_list, 'c_list' : c_list})

@user_passes_test(email_check)
# @wrong_email
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
		exercices = Exercice.objects.filter(nom__contains=searched) | Exercice.objects.filter(tags__name__icontains=searched)
		return render(request, 'exo/search_chap.html', {'searched' : searched,
			'chapitres' : chapitres, 'exercices' : exercices})
	return render(request, 'exo/search_chap.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def upload_fichier(request, pk):
	exercice = Exercice.objects.get(id=pk)
	if request.method == "POST":
		form = FichierForm(request.POST , request.FILES, initial={'exercice': exercice})
		if form.is_valid():
			fichier = form.save(commit = False)
			fichier.save()
			return redirect('exercice-details', exercice_id = fichier.exercice.pk)
	else:
		form = FichierForm(initial={'exercice': exercice})
	return render(request, 'exo/up_fichier.html', {'form': form,})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def supp_ex(request, exercice_id):
	exercice = Exercice.objects.get(pk=exercice_id)
	exercice.delete()
	return redirect('/exercices/')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def supp_chap(request, chapitre_id):
	chapitre = Chapitre.objects.get(pk=chapitre_id)
	chapitre.delete()
	return redirect('/chapitres/')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def add_ex(request):
	if request.method == "POST":
		form = ExerciceForm(request.POST)
		if form.is_valid():
			exercice = form.save(commit=False)
			exercice.save()
			form.save_m2m()
			return redirect('exercice-details', exercice_id = exercice.pk)
	else:
		form = ExerciceForm()
	return render(request, 'exo/new_ex.html', {'form': form,})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def add_exchap(request, pk):
	chapitre = Chapitre.objects.get(id=pk)
	if request.method == "POST":
		form = ExerciceForm(request.POST, initial={'chapitre': chapitre})
		if form.is_valid():
			exercice = form.save(commit=False)
			exercice.save()
			form.save_m2m()
			return redirect('exercice-details', exercice_id = exercice.pk)
	else:
		form = ExerciceForm(initial={'chapitre': chapitre})
	return render(request, 'exo/new_ex.html', {'form': form,})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
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
    paginate_by = 10
    ordering = ['nom']

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def exercice_edit(request, exercice_id):
	exercice = get_object_or_404(Exercice, pk=exercice_id)
	if request.method == "POST":
		form = ExerciceForm(request.POST, instance=exercice)
		if form.is_valid():
			exercice = form.save(commit=False)
			exercice.save()
			form.save_m2m()
			return redirect('exercice-details', exercice_id = exercice.pk)
	else:
		form = ExerciceForm(instance=exercice)
	return render(request, 'exo/edit_ex.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def chapitre_edit(request, chapitre_id):
	chapitre = get_object_or_404(Chapitre, pk=chapitre_id)
	if request.method == "POST":
		form = ChapitreForm(request.POST, instance=chapitre)
		if form.is_valid():
			chapitre = form.save(commit=False)
			chapitre.save()
			form.save_m2m()
			return redirect('chapitre-details', chapitre_id = chapitre.pk)
	else:
		form = ChapitreForm(instance=chapitre)
	return render(request, 'exo/edit_chap.html', {'form': form})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def edit_fichier(request, pk):
	fichier = get_object_or_404(Fichier, pk=pk)
	if request.method == "POST":
		form = FichierForm(request.POST, request.FILES, instance=fichier)
		if form.is_valid():
			fichier = form.save(commit=False)
			fichier.save()
			return redirect('exercice-details', exercice_id = fichier.exercice.pk)
	else:
		form = FichierForm(instance=fichier)
	return render(request, 'exo/edit_fichier.html', {'form': form})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def supp_fichier(request, pk):
	fichier = Fichier.objects.get(pk=pk)
	exercice_id = fichier.exercice.pk
	if request.method == "POST":
		fichier.delete()
	return redirect('exercice-details', exercice_id = exercice_id)

@login_required(login_url='login')
def exercice_filtres(request):
	exercices = Exercice.objects.all()
	myFilter = ExerciceFilter(request.GET, queryset=exercices)
	exercices = myFilter.qs
	context = {'exercices': exercices, 'myFilter': myFilter}
	return render(request, 'exo/exercice_filtres.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'prof'])
def add_util(request, pk):
	exercice = Exercice.objects.get(id=pk)
	if request.method == "POST":
		form = UtilisationForm(request.POST, initial={'exercice': exercice})
		if form.is_valid():
			exercice = form.save(commit=False)
			exercice.save()
			return redirect('exercice-details', exercice_id = exercice.pk)
	else:
		form = UtilisationForm(initial={'exercice': exercice})
	return render(request, 'exo/new_util.html', {'form': form,})