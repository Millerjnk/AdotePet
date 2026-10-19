from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from django.views.decorators.http import require_http_methods
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
        'pode_gerenciar': (
            request.user.is_authenticated
            and request.user.tipo_usuario == 'R'
            and pet.responsavel_id == request.user.pk
        ),
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


def _pet_do_responsavel(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if request.user.tipo_usuario != 'R' or pet.responsavel_id != request.user.pk:
        raise PermissionDenied('Somente o responsável por este pet pode alterá-lo.')
    return pet


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def editar_pet(request, pk):
    pet = _pet_do_responsavel(request, pk)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet atualizado com sucesso!')
            return redirect('detalhe_pet', pk=pet.pk)
        messages.error(request, 'Não foi possível atualizar o pet. Confira os campos abaixo.')
    else:
        form = PetForm(instance=pet)
    form.fields['data_nascimento'].widget.format = '%Y-%m-%d'
    return render(request, 'pets/editar_pet.html', {'form': form, 'pet': pet})


@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def remover_pet(request, pk):
    pet = _pet_do_responsavel(request, pk)
    if request.method == 'POST':
        try:
            pet.delete()
        except ProtectedError:
            messages.error(
                request,
                'Este pet possui solicitações de adoção e não pode ser removido. '
                'O histórico de adoções deve ser preservado.'
            )
            return redirect('detalhe_pet', pk=pet.pk)
        messages.success(request, 'Pet removido com sucesso!')
        return redirect('lista_pets')
    return render(request, 'pets/remover_pet.html', {
        'pet': pet,
        'possui_solicitacoes': pet.aplicacoes_adocao.exists(),
    })
