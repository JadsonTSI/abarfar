from django.db import models
from contas.models import Perfil

# bd de ensaios

class EnsaiosproModel(models.Model):
    DIAS_SEMANA = [
        ("Segunda-feira", "Segunda-feira"),
        ("Terça-feira", "Terça-feira"),
        ("Quarta-feira", "Quarta-feira"),
        ("Quinta-feira", "Quinta-feira"),
        ("Sexta-feira", "Sexta-feira"),
        ("Sábado", "Sábado"),
        ("Domingo", "Domingo"),
    ]

    nome = models.CharField(max_length=100)
    dia_semana = models.CharField(max_length=20, choices=DIAS_SEMANA)
    data = models.DateField()
    inicio = models.TimeField()
    fim = models.TimeField()
    local = models.CharField(max_length=150)
    cancelado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.nome} - {self.data}"

    class Meta:
        ordering = ["data", "inicio"]


# bd de apresentações

class ApresentacaoModel(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=200)
    data = models.DateField()
    horario = models.CharField(max_length=100)
    local = models.CharField(max_length=150)
    grupo = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} - {self.descricao}"
    

# bd cadastro professor

class ProfessorModel(models.Model):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    instrumento = models.CharField(max_length=100)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome