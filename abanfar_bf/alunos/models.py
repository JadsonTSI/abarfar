from django.db import models
from contas.models import Perfil

class Aluno(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    nome = models.CharField(max_length=150)
    sobrenome = models.CharField(max_length=150)
    matricula = models.CharField(max_length=30, unique=True)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nome} {self.sobrenome} - {self.matricula}"
    
