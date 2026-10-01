from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Especie, Raca, Usuario, Pet, RegistroMedico, CronogramaVisita

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
    list_display=("nome", "raca", "cor", "sexo", "status")
    list_filter=("sexo", "porte", "raca")
    search_fields=("nome","raca__especie__nome","raca__nome")
    ordering=("nome",)

@admin.register(RegistroMedico)
class RegistroMedicoAdmin(admin.ModelAdmin):
    list_display=("data", "pet", "tipo", "descricao")
    list_filter=("tipo", "data")
    search_fields=("pet__nome", "tipo", "veterinario", "clinica",)
    ordering=("-data",)

@admin.register(CronogramaVisita)
class VisitasAdmin(admin.ModelAdmin):
    list_display=("pet", "adotante", "data", "horario", "local", "status")
    list_filter=("data", "status")
    search_fields=("pet__nome", "adotante__username", "adotante__first_name", "adotante__last_name",)
    ordering=("-data", "horario",)