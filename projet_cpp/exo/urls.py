from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('exercices/', views.ExerciceListView.as_view(), name='exercices'),
    path('exercice/<int:exercice_id>', views.detail, name='exercice-details'),
    path('1A', views.all_1A, name="1A"),
    path('2A', views.all_2A, name="2A"),
    path('maths_1A', views.maths_1A, name="1A-maths"),
    path('phys_1A', views.phys_1A, name="1A-physique"),
    path('chim_1A', views.chim_1A, name="1A-chimie"),
    path('maths_2A', views.maths_2A, name="2A-maths"),
    path('phys_2A', views.phys_2A, name="2A-physique"),
    path('chim_2A', views.chim_2A, name="2A-chimie"),
    path('addformat/<int:pk>' , views.upload_fichier, name='nouv_fichier'),
    path('supp_ex/<int:exercice_id>', views.supp_ex, name='supp_ex'),
    path('supp_chap/<int:chapitre_id>', views.supp_chap, name='supp_chap'),
    path('addexercice/', views.add_ex, name='new_ex'),
    path('addexercice/<int:pk>', views.add_exchap, name='new_exchap'),
    path('chapitre/<int:chapitre_id>', views.chap_detail, name='chapitre-details'),
    path('addchapitre/', views.add_chap, name='new_chap'),
    path('chapitres/', views.ChapitreListView.as_view(), name='chapitres'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('edit_ex/<int:exercice_id>', views.exercice_edit, name='edit_ex'),
    path('edit_chap/<int:chapitre_id>', views.chapitre_edit, name='edit_chap'),
    path('edit_fichier/<int:pk>', views.edit_fichier, name='edit_fichier'),
    path('supp_fichier/<int:pk>', views.supp_fichier, name='supp_fichier'),
    path('filtres/', views.exercice_filtres, name='exercice_filtres'),
    
]