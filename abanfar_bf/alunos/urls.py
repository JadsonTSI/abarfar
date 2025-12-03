from django.urls import path
from . import views

app_name = "alunos"

urlpatterns = [
    path("cadastrar/", views.cadastrar_aluno, name="cadastrar"),
    path("sucesso/", views.sucesso, name="sucesso"),
    path("ensaios/", views.ensaios_aluno, name="ensaios"),
    path("ensaios/", views.ensaios_aluno, name="ensaios_aluno"),
    path("apresentacoes/", views.apresentacoes_aluno, name="apresentacoes"),

]
