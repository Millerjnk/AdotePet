from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404 ,redirect, render
from .forms import PetForm
from .models import Pet, RegistroMedico

User = get_user_model()

def lista_pets(request):
    query = request.GET.get('q', '')
    especie_id = request.GET.get('especie', '')
    porte = request.GET.get('porte', '')
    sexo = request.GET.get('sexo', '')

    pets = Pet.objects.all().order_by('-id')

    if query:
        pets = pets.filter(nome__icontains= query)
    if especie_id:
        pets = pets.filter(raca__especie =especie_id)
    if porte:
        pets = pets.filter(porte=porte)
    if sexo:
        pets = pets.filter(sexo=sexo)           
    
    paginator = Paginator(pets, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }

    return render (request, 'pets/lista_pets.html', context)

def detalhe_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    r_medicos = RegistroMedico.objects.filter(pet=pet)

    context = {
        'pet': pet,
        'registros_medicos': r_medicos,
    }

    return render(request, 'pets/detalhe_pet.html', context)

@login_required
def cadastrar_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            if request.user.is_authenticated:
                pet.responsavel = request.user
            else:
                pet.responsavel = User.objets.first()
            pet.save()
            messages.success(request, 'Pet cadastrado com sucesso!')
            return redirect('lista_pets')
        else:
            messages.error(request, 'ERRO! Não foi possível cadastrar o pet.')
    else:
        form = PetForm()

    return render(request, 'pets/cadastrar_pet.html', {'form': form})
