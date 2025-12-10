from django.db import models
from alunos.models import GrupoMusical

class Partitura(models.Model):
    grupo = models.ForeignKey(GrupoMusical, on_delete=models.CASCADE, related_name="partituras")
    titulo = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to="partituras/")
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.grupo.nome})"
