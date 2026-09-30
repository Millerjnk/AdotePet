from django.db import models


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

# Create your models here.
