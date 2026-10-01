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
        ('Outro', 'Outro')
    ]
TIPOS_USUARIO = [
    ('A', 'Adotante'),
    ('R', 'Responsável')
]
TIPO_MORADIA = [
    ('A', 'Apartamento'),
    ('C', 'Casa'),
    ('O', 'Outro')
]

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

class AplicacaoAdocao(models.Model):
    STATUS = [
        ('P', 'Pendente'),
        ('A', 'Aprovada'),
        ('R', 'Rejeitada'),
        ('C', 'Cancelada'),
    ]

    pet = models.ForeignKey(Pet, on_delete=models.PROTECT, related_name="aplicacoes_adocao")
    adotante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="aplicacoes_adocao")
    data_solicitacao = models.DateField()
    status = models.CharField(max_length=1,choices=STATUS,default='P')
    motivacao = models.TextField()
    outros_animais = models.BooleanField(default=False)
    tipo_moradia = models.CharField(max_length=1, choices=TIPO_MORADIA)

    class Meta:
        verbose_name = "Aplicação de Adoção"
        verbose_name_plural = "Aplicações de Adoção"
        ordering = ["-data_solicitacao"]
        unique_together = ("pet", "adotante")
    def __str__(self):
        return f"{self.pet} - {self.adotante} - {self.get_status_display()}"
    
class CronogramaVisita(models.Model):
    aplicacao = models.ForeignKey(AplicacaoAdocao, on_delete=models.PROTECT, related_name="visitas")
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
        return f"{self.aplicacao.pet} - {self.aplicacao.adotante} - {self.data}"

class TermoAdocao(models.Model):
    aplicacao = models.OneToOneField(AplicacaoAdocao, on_delete=models.PROTECT, related_name="termo_adocao")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="termo_responsavel")
    data_adocao = models.DateField()
    termos_aceitos = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    class Meta:
        verbose_name = "Termo de Adoção"
        verbose_name_plural = "Termos de Adoção"
        ordering = ["-data_adocao"]
    def __str__(self):
        return f"{self.aplicacao.pet} - {self.aplicacao.adotante} - {self.responsavel}"
