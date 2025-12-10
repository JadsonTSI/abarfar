from django.db import models
from professores.models import ProfessorModel
from alunos.models import Aluno

class Materia(models.Model):
    nome = models.CharField(max_length=120)
    professor = models.ForeignKey(ProfessorModel, on_delete=models.SET_NULL, null=True)
    google_classroom_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nome


class MatriculaMateria(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_matricula = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno} → {self.materia}"