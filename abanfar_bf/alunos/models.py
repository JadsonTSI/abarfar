from django.db import models
from contas.models import Perfil
from instrumentos.models import Instrumento  # <-- IMPORTA O INSTRUMENTO CERTO!


class Naipe(models.Model):
    nome = models.CharField(max_length=100)
    instrumentos = models.ManyToManyField(Instrumento, related_name="naipes", blank=True)

    def __str__(self):
        return self.nome


class GrupoMusical(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)

    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=30, unique=True)
    telefone = models.CharField(max_length=20, blank=True)

    instrumento = models.ForeignKey(
        Instrumento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    naipe = models.ForeignKey(
        Naipe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    grupo = models.ForeignKey(
        GrupoMusical,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    funcao = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ex: Violino 1, Violino 2, Flauta 1, Trompete Solo..."
    )

    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.matricula}"
