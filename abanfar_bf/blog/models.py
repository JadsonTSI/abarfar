from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    titulo = models.CharField("Título", max_length=200)
    tag = models.CharField("Tag/Categoria", max_length=50)
    slug = models.SlugField("Slug", unique=True, max_length=200, blank=True)
    resumo = models.TextField("Resumo")
    conteudo = models.TextField("Conteúdo")
    imagem_estatica = models.CharField("Imagem Estática", max_length=100, blank=True, null=True)
    data_publicacao = models.DateField("Data de Publicação")
    autor = models.CharField("Autor", max_length=100, default="Equipe ABANFAR BF")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo


class MensagemContato(models.Model):
    nome = models.CharField("Nome", max_length=120)
    email = models.EmailField("E-mail")
    assunto = models.CharField("Assunto", max_length=150)
    mensagem = models.TextField("Mensagem")
    criada_em = models.DateTimeField("Recebida em", auto_now_add=True)
    lida = models.BooleanField("Lida", default=False)

    class Meta:
        verbose_name = "Mensagem de contato"
        verbose_name_plural = "Mensagens de contato"
        ordering = ["-criada_em"]

    def __str__(self):
        return f"{self.nome} — {self.assunto}"


class InscricaoNewsletter(models.Model):
    email = models.EmailField("E-mail", unique=True)
    criada_em = models.DateTimeField("Inscrito em", auto_now_add=True)

    class Meta:
        verbose_name = "Inscrição na newsletter"
        verbose_name_plural = "Inscrições na newsletter"
        ordering = ["-criada_em"]

    def __str__(self):
        return self.email
