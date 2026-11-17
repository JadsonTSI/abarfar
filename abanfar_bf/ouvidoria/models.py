import secrets

from django.db import models
from django.utils import timezone

# Sem caracteres que se confundem (0/O, 1/I/L)
ALFABETO_PROTOCOLO = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"


def gerar_protocolo():
    """Protocolo difícil de adivinhar, ex.: OUV-2026-K7M4QX9P.

    Quem tem o protocolo consegue ver a resposta, então ele não pode ser sequencial.
    """
    codigo = "".join(secrets.choice(ALFABETO_PROTOCOLO) for _ in range(8))
    return f"OUV-{timezone.now().year}-{codigo}"


class Manifestacao(models.Model):
    class Tipo(models.TextChoices):
        RECLAMACAO = "reclamacao", "Reclamação"
        SUGESTAO = "sugestao", "Sugestão"
        ELOGIO = "elogio", "Elogio"
        DENUNCIA = "denuncia", "Denúncia"
        SOLICITACAO = "solicitacao", "Solicitação de informação"

    class Status(models.TextChoices):
        RECEBIDA = "recebida", "Recebida"
        EM_ANALISE = "em_analise", "Em análise"
        RESPONDIDA = "respondida", "Respondida"
        ENCERRADA = "encerrada", "Encerrada"

    protocolo = models.CharField("Protocolo", max_length=20, unique=True, editable=False)
    tipo = models.CharField("Tipo", max_length=20, choices=Tipo.choices)
    anonima = models.BooleanField("Anônima", default=False)
    nome = models.CharField("Nome", max_length=120, blank=True)
    email = models.EmailField("E-mail", blank=True)
    telefone = models.CharField("Telefone", max_length=30, blank=True)
    assunto = models.CharField("Assunto", max_length=150)
    mensagem = models.TextField("Relato")

    status = models.CharField("Situação", max_length=20, choices=Status.choices, default=Status.RECEBIDA)
    resposta = models.TextField("Resposta ao manifestante", blank=True)
    respondida_em = models.DateTimeField("Respondida em", null=True, blank=True)
    observacoes_internas = models.TextField(
        "Observações internas", blank=True,
        help_text="Visível apenas para a equipe; não aparece para o manifestante.",
    )

    criada_em = models.DateTimeField("Recebida em", auto_now_add=True)
    atualizada_em = models.DateTimeField("Atualizada em", auto_now=True)

    class Meta:
        verbose_name = "Manifestação"
        verbose_name_plural = "Manifestações"
        ordering = ["-criada_em"]

    def __str__(self):
        return f"{self.protocolo} — {self.get_tipo_display()}"

    def save(self, *args, **kwargs):
        if not self.protocolo:
            protocolo = gerar_protocolo()
            while Manifestacao.objects.filter(protocolo=protocolo).exists():
                protocolo = gerar_protocolo()
            self.protocolo = protocolo
        if self.anonima:
            # Anônima de verdade: não guarda dados de identificação
            self.nome = self.email = self.telefone = ""
        super().save(*args, **kwargs)
