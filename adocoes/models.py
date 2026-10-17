from django.db import models
from django.conf import settings
from pets.models import Pet 

STATUS_VISITA = [
    ('A', 'Agendada'),
    ('R', 'Realizada'),
    ('C', 'Cancelada')
]
TIPO_MORADIA = [
    ('A', 'Apartamento'),
    ('C', 'Casa'),
    ('O', 'Outro')
]

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