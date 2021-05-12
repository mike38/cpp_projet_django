from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercices/', views.ExerciceListView.as_view(), name='exercices'),
    path('exercice/<int:exercice_id>', views.detail, name='exercice-details'),
    path('format/' , views.upload_fichier, name='newformat')
    
]