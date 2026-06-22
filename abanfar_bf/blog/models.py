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
