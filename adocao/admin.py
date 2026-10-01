from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Especie, Raca, Usuario, Pet, RegistroMedico, CronogramaVisita, TermoAdocao, AplicacaoAdocao, Endereco


class EnderecoInline(admin.StackedInline):
    model= Endereco
    extra= 0
    max_num=1 

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    inlines = [EnderecoInline]
    fieldsets = UserAdmin.fieldsets + (
            ("Informações do AdotePet", {"fields": ("tipo_usuario", "telefone")}),
        )
    add_fieldsets = UserAdmin.add_fieldsets + (
            ("Informações do AdotePet", {"fields": ("tipo_usuario", "telefone")}),
        )
    
@admin.register(Especie)
class EspecieAdmin(admin.ModelAdmin):
    list_display=("id","nome")
    search_fields=("nome",)
    ordering=("nome",)

@admin.register(Raca)
class RacaAdmin(admin.ModelAdmin):
    list_display=("id", "nome", "especie")
    list_filter=("especie",)
    search_fields=("nome", "especie__nome")
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

@admin.register(AplicacaoAdocao)
class AplicacaoAdocaoAdmin(admin.ModelAdmin):
    list_display = ("pet", "adotante", "data_solicitacao", "status")
    list_filter = ("status", "data_solicitacao")
    search_fields = (
        "pet__nome",
        "adotante__username",
        "adotante__first_name",
        "adotante__last_name",
    )
    ordering = ("-data_solicitacao",)

@admin.register(CronogramaVisita)
class VisitasAdmin(admin.ModelAdmin):
    list_display=("pet", "adotante", "data", "horario", "local", "status")
    list_filter=("data", "status")
    search_fields=("aplicacao__pet__nome", "aplicacao__adotante__username", "aplicacao__adotante__first_name", "aplicacao__adotante__last_name",)
    ordering=("-data", "horario",)

    def pet(self, obj):
        return obj.aplicacao.pet

    def adotante(self, obj):
        return obj.aplicacao.adotante

@admin.register(TermoAdocao)
class TermoAdocaoAdmin(admin.ModelAdmin):
    list_display=("pet", "adotante", "responsavel", "data_adocao")
    list_filter=("data_adocao", "termos_aceitos")
    search_fields=(
        "aplicacao__pet__nome", 
        "aplicacao__adotante__username", 
        "aplicacao__adotante__first_name", 
        "aplicacao__adotante__last_name", 
        "responsavel__username", 
        "responsavel__first_name", 
        "responsavel__last_name",)
    ordering=("-data_adocao",)

    def pet(self, obj):
        return obj.aplicacao.pet
    
    def adotante(self, obj):
        return obj.aplicacao.adotante