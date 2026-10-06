from django.contrib import admin
from adocoes.models import AplicacaoAdocao, CronogramaVisita, TermoAdocao

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