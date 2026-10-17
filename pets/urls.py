from django.urls import path
from . import views

urlpatterns=[
    path('', views.lista_pets, name='lista_pets'),
]