from django.urls import path
from . import views

urlpatterns=[
    path('', views.lista_pets, name='lista_pets'),
    path('<int:pk>/', views.detalhe_pet, name='detalhe_pet'),
    path('cadastrar/', views.cadastrar_pet, name = 'cadastrar_pet'),
]