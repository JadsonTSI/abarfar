from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Perfil(models.Model):
    TIPOS = (
        ('gerente', 'Gerente'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    foto = models.ImageField(upload_to="perfil_fotos/", null=True, blank=True)


    def __str__(self):
        return f"{self.user.username} - {self.tipo}"

