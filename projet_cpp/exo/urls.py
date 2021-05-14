from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercices/', views.ExerciceListView.as_view(), name='exercices'),
    path('exercice/<int:exercice_id>', views.detail, name='exercice-details'),
    path('1A', views.all_1A, name="1A"),
    path('2A', views.all_2A, name="2A"),
    path('format/' , views.upload_fichier, name='newformat'),
    path('supp_ex/<int:exercice_id>', views.supp_ex, name='supp_ex'),
    path('addexercice/', views.add_ex, name='new_ex'),
    
]