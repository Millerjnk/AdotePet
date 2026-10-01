from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

PORTES = [
        ('P','Pequeno'),
        ('M','Médio'),
        ('G','Grande')
    ]
SEXOS = [
    ('M', 'Macho'),
    ('F', 'Fêmea')
]
STATUS_ADOÇAO = [
    ('D', 'Disponível'),
    ('A', 'Em Andamento'),
    ('C', 'Adotado')
]
STATUS_VISITA = [
    ('A', 'Agendada'),
    ('R', 'Realizada'),
    ('C', 'Cancelada')
]
TIPOS = [
        ('Vacina', 'Vacina'),
        ('Consulta', 'Consulta'),
        ('Exame', 'Exame'),
        ('Medicação', 'Medicação'),
        ('Cirurgia', 'Cirurgia'),
        ('Castração', 'Castração'),
        ('Outro', 'Outro'),
    ]

class Usuario(AbstractUser):
    pass

class Especie(models.Model):
    nome =models.CharField(max_length=100, unique=True)
    class Meta:
        verbose_name= "Espécie"
        verbose_name_plural= "Espécies" 
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
        verbose_name_plural="Raças"
        ordering=["nome"]
        unique_together=("nome","especie")
    def __str__(self):
        return f"{self.nome} ({self.especie.nome})"

class Pet(models.Model):
    nome= models.CharField(max_length=100)
    cor = models.CharField(max_length=50)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXOS)
    porte = models.CharField(max_length=1, choices=PORTES)
    peso = models.DecimalField(max_digits=5,decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_ADOÇAO, default='D')
    raca = models.ForeignKey(Raca, on_delete=models.PROTECT, related_name="pets")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pets")
    foto = models.ImageField(upload_to='pets/', null= True, blank=True)  # Definido assim temporariamente
    class Meta:
            verbose_name= "Pet"
            verbose_name_plural= "Pets"
            ordering= ["nome"]
    def __str__(self):
        return self.nome

class RegistroMedico(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="registros_medicos")
    tipo = models.CharField(max_length=15, choices=TIPOS)
    data = models.DateField()
    descricao_outro = models.CharField(max_length=100, blank=True)
    descricao = models.TextField()
    veterinario = models.CharField(max_length=100, blank=True)
    clinica = models.CharField(max_length=100, blank=True)
    class Meta:
        verbose_name= "Registro Médico"
        verbose_name_plural= "Registros Médicos"
        ordering= ["-data"]
    def __str__(self):
        return f"{self.tipo} - {self.pet} - {self.data}"

class CronogramaVisita(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name="visitas")
    adotante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="visitas")
    data = models.DateField()
    horario = models.TimeField()
    local = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=STATUS_VISITA, default='A')
    observacoes = models.TextField(blank=True)
    class Meta:
        verbose_name= "Visita"
        verbose_name_plural= "Visitas"
        ordering= ["-data", "horario"]
    def __str__(self):
        return f"{self.pet} - {self.adotante} - {self.data}"

class TermoAdocao(models.Model):
    pet = models.OneToOneField(Pet, on_delete=models.PROTECT, related_name="termo_adocao")
    adotante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="termo_adotante")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="termo_responsavel")
    data_adocao = models.DateField()
    termos_aceitos = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    class Meta:
        verbose_name = "Termo de Adoção"
        verbose_name_plural = "Termos de Adoção"
        ordering = ["-data_adocao"]
    def __str__(self):
        return f"{self.pet} - {self.adotante} - {self.responsavel}"
