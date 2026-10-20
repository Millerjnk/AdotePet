from django.urls import path
from . import views

urlpatterns=[
    path('<int:pk>/editar/', views.editar_pet, name='editar_pet'),
    path('<int:pk>/remover/', views.remover_pet, name='remover_pet'),
    path('', views.lista_pets, name='lista_pets'),
    path('<int:pk>/', views.detalhe_pet, name='detalhe_pet'),
    path('cadastrar/', views.cadastrar_pet, name = 'cadastrar_pet'),
]