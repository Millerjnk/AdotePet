from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Especie, Usuario

admin.site.register(Usuario, UserAdmin)

@admin.register(Especie)
class EspecieAdimin(admin.ModelAdmin):
    list_display=("id","nome")
    search_fields=("nome",)
    ordering=("nome",)
# Register your models here.
