from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Perfil
from alunos.models import Aluno
from professores.models import ProfessorModel
from materias.models import Materia, MatriculaMateria


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        senha = request.POST.get("senha")

        user = authenticate(request, username=username, password=senha)

        if user:
            login(request, user)
            perfil = Perfil.objects.get(user=user)

            if perfil.tipo == "gerente":
                return redirect("contas:painel_gerente")
            elif perfil.tipo == "professor":
                return redirect("professores:professoreshome")
            elif perfil.tipo == "aluno":
                return redirect("contas:painel_aluno")

        messages.error(request, "Usuário ou senha incorretos!")
        return redirect("contas:login")

    return render(request, "contas/login.html")


def logout_view(request):
    logout(request)
    return redirect("contas:login")


def painel_gerente(request):
    return render(request, "contas/gerente_home.html")


def painel_professor(request):
    return render(request, "contas/professor.html")


def painel_aluno(request):
    perfil = request.user.perfil
    aluno = perfil.aluno
    return render(request, "contas/aluno_home.html", {"perfil": perfil, "aluno": aluno})



def lista_alunos(request):
    alunos = Aluno.objects.all()
    return render(request, "contas/gerente_lista_alunos.html", {"alunos": alunos})



def perfil_view(request):
    perfil = request.user.perfil

    aluno = None
    professor = None
    materias = []

    # --- Se for aluno ---
    try:
        aluno = perfil.aluno
        materias = Materia.objects.filter(
            id__in=MatriculaMateria.objects.filter(aluno=aluno).values("materia")
        )
    except:
        aluno = None

    # --- Se for professor ---
    try:
        professor = perfil.professor  # ✅ AGORA ESTÁ CORRETO
        materias = Materia.objects.filter(professor=professor)
    except:
        professor = None

    contexto = {
        "perfil": perfil,
        "aluno": aluno,
        "professor": professor,
        "materias": materias,
    }

    return render(request, "contas/perfil.html", contexto)


def alterar_foto(request):
    perfil = request.user.perfil

    if request.method == "POST" and request.FILES.get("foto"):
        perfil.foto = request.FILES["foto"]
        perfil.save()

    return redirect("contas:perfil")