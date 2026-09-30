from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    pass

class Especie(models.Model):
    nome =models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name= "Especie"
        verbose_name_plural= "Especies" 
        ordering = ["nome"]
    def __str__(self):
        return self.nome

class Raca(models.Model):
    nome=models.CharField(max_length=100)
    especie = models.ForeignKey(
        Especie,on_delete=models.CASCADE,related_name="racas"
    )
    class Meta:
        verbose_name="Raça"
        verbose_name="Raças"
        ordering=["nome"]
        unique_together=("nome","especie")
    def __str__(self):
        return f"{self.nome} ({self.especie.nome})"

class Pet(models.Model):
    nome= models.CharField(max_length=100)
    cor = models.CharField(max_length=50)
    data_nascimento = models.DateField(null=True, blank=True)
    PORTES = [
        ('P','Pequeno'),
        ('M','Médio'),
        ('G','Grande')
    ]
    SEXOS = [
        ('M', 'Macho'),
        ('F', 'Fêmea')
    ]
    STATUS = [
        ('D', 'Disponível'),
        ('A', 'Em Andamento'),
        ('C', 'Adotado')
    ]
    sexo = models.CharField(max_length=1, choices=SEXOS)
    porte = models.CharField(max_length=1, choices=PORTES)
    peso = models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='Disponível')
    raca = models.ForeignKey(Raca, on_delete=models.PROTECT, related_name="pets")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pets")
    foto = models.ImageField(upload_to='pets/', null= True, blank=True)  # Definido assim temporariamente 

# Create your models here.
