from django.db import models
from django.utils import timezone
import uuid

class Instrumento(models.Model):
    nome = models.CharField(max_length=100)
    identificador = models.CharField(max_length=20, unique=True, blank=True)
    descricao = models.TextField(blank=True)
    pertence_associacao = models.BooleanField(default=True)
    ativo = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        # Se ainda não existir número de série → gerar um novo
        if not self.identificador:
            ultimo = Instrumento.objects.order_by('-id').first()

            if ultimo:
                novo_num = ultimo.id + 1
            else:
                novo_num = 1

            # Formatação: INS-0001
            self.identificador = f"INS-{novo_num:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.identificador})"


class InstrumentoEmprestimo(models.Model):
    instrumento = models.ForeignKey(Instrumento, on_delete=models.CASCADE)
    aluno = models.ForeignKey("alunos.Aluno", on_delete=models.CASCADE)  # string reference
    data_emprestimo = models.DateField(default=timezone.now)
    data_devolucao = models.DateField(blank=True, null=True)
    devolvido = models.BooleanField(default=False)
    observacao = models.TextField(blank=True)

    def __str__(self):
        return f"{self.instrumento.identificador} -> {self.aluno.matricula} ({'devolvido' if self.devolvido else 'emprestado'})"
