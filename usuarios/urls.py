from django.urls import path
from . import views

urlpatterns = [
        path('', views.telaLogin, name='login')
]
