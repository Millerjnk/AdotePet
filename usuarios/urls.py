from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
        path('', views.telaLogin, name='login'),
        path('logout/', LogoutView.as_view(next_page='lista_pets'), name='logout'),
]
