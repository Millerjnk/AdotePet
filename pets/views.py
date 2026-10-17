from django.shortcuts import render
from .models import Pet

def lista_pets(request):
    pets=Pet.objects.filter(status='D').select_related(
        'raca',
        'raca__especie'
    ).order_by('nome')

    return render (request, 'pets/lista_pets.html',{
        'pets': pets
    })