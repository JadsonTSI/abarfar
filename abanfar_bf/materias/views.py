from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Materia, MatriculaMateria
from professores.models import ProfessorModel
from alunos.models import Aluno

# --------------------
# GERENTE
# --------------------

def lista_materias_gerente(request):
    materias = Materia.objects.all()
    return render(request, "materias/gerente_lista.html", {"materias": materias})


def criar_materia(request):
    professores = ProfessorModel.objects.all()

    if request.method == "POST":
        nome = request.POST.get("nome")
        professor_id = request.POST.get("professor")

        professor = ProfessorModel.objects.get(id=professor_id)

        Materia.objects.create(nome=nome, professor=professor)
        return redirect("materias:materias_gerente")

    return render(request, "materias/gerente_criar.html", {"professores": professores})


def matricular_alunos(request, materia_id):
    materia = Materia.objects.get(id=materia_id)
    alunos = Aluno.objects.all()

    if request.method == "POST":
        aluno_id = request.POST.get("aluno")
        aluno = Aluno.objects.get(id=aluno_id)

        MatriculaMateria.objects.get_or_create(materia=materia, aluno=aluno)
        return redirect("materias:materias_gerente")

    return render(request, "materias/gerente_matricular.html", {"materia": materia, "alunos": alunos})


# --------------------
# PROFESSOR
# --------------------

@login_required
def minhas_materias_professor(request):
    professor = request.user.perfil.professor  # Perfil → ProfessorModel
    materias = Materia.objects.filter(professor=professor)
    return render(request, "materias/professor_lista.html", {"materias": materias})


@login_required
def editar_link(request, materia_id):
    professor = request.user.perfil.professor
    materia = Materia.objects.get(id=materia_id, professor=professor)

    if request.method == "POST":
        materia.google_classroom_link = request.POST.get("link")
        materia.save()
        return redirect("materias:materias_professor")

    return render(request, "materias/professor_editar_link.html", {"materia": materia})


# --------------------
# ALUNO
# --------------------

@login_required
def materias_aluno(request):
    aluno = request.user.perfil.aluno
    matriculas = MatriculaMateria.objects.filter(aluno=aluno).select_related("materia")
    return render(request, "materias/aluno_lista.html", {"matriculas": matriculas})
