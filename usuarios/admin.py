from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from usuarios.models import Usuario, Endereco

# Register your models here.
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