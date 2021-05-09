from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('exercices/', views.ExerciceListView.as_view(), name='exercices'),
    path('exercice/<int:pk>', views.ExerciceDetailView.as_view(), name='exercice-details'),
]