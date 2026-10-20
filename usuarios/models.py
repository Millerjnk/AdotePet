from django.db import models
from django.contrib.auth.models import AbstractUser

TIPOS_USUARIO = [
    ('A', 'Adotante'),
    ('R', 'Responsável')
]

# Create your models here.
class Usuario(AbstractUser):
    tipo_usuario = models.CharField(max_length=1, choices=TIPOS_USUARIO, default='A')
    telefone = models.CharField(max_length=20)
    
class Endereco(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="endereco")
    cep= models.CharField(max_length=9)
    logradouro = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    uf = models.CharField(max_length=2)
    class Meta:
        verbose_name="Endereço"
        verbose_name_plural="Endereços"
        ordering=["usuario"]
    def __str__(self):
        return f"{self.usuario} - {self.cidade}/{self.uf}"