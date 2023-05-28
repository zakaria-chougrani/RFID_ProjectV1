from django.urls import path

from . import views

urlpatterns = [
    path('inscription/', views.inscriptionPage, name='inscription'),
    path('acces/', views.accesPage, name='acces'),
    path('quitter/', views.logoutPage, name='quitter'),
    ]