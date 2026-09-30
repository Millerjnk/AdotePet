from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Especie, Raca, Usuario, Pet

admin.site.register(Usuario, UserAdmin)

@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display=("id","nome")
    search_fields=("nome",)
    ordering=("nome",)

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display=("id", "nome", "especie")
    list_filter=("especie",)
    search_fields=("nome", "especie_nome")
    ordering=("nome",)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display=("id", "nome", "raca", "cor")
    list_filter=("sexo", "porte", "raca")
    search_fields=("raca__especie__nome","raca__nome")
    ordering=("nome",)
