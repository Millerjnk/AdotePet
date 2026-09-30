from django.db import models
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
# Create your models here.
