from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('add/', views.add_note, name='add_note'),
    path('notes/', views.view_notes, name='view_notes'),
]