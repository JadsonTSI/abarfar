from django.urls import path
from . import views

app_name = "materias"

urlpatterns = [
    path("professor/", views.minhas_materias_professor, name="materias_professor"),
    path("professor/<int:materia_id>/editar/", views.editar_link, name="editar_link"),

    path("aluno/", views.materias_aluno, name="materias_aluno"),

    path("gerente/", views.lista_materias_gerente, name="materias_gerente"),
    path("gerente/criar/", views.criar_materia, name="criar_materia"),
    path("gerente/<int:materia_id>/matricular/", views.matricular_alunos, name="matricular_alunos"),
]
