from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Usuario

# Create your views here.
def telaLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.tipo_usuario == 'A':
                return redirect('lista_pets')

            elif user.tipo_usuario == 'R':
                return redirect('lista_pets')

            else:
                return render(request, 'registration/login.html', {
                    'erro': 'Tipo de usuário inválido.'
                })

        return render(request, 'registration/login.html', {
            'erro': 'Usuário ou senha incorretos.'
        })

    return render(request, 'registration/login.html')

