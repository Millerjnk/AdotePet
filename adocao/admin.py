from django.contrib import admin
from .models import Especie

@admin.register(Especie)
class EspecieAdimin(admin.ModelAdmin):
    list_display=("id","nome")
    search_fields=("nome",)
    ordering=("nome",)
# Register your models here.
