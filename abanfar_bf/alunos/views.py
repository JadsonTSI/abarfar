from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AlunoCadastroForm, AlunoForm
from professores.models import EnsaiosproModel, ApresentacaoModel
from .models import Aluno, Instrumento, Naipe, GrupoMusical 


# -------------------------
# CADASTRAR ALUNO
# -------------------------

def cadastrar_aluno(request):
    form = AlunoCadastroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("alunos:sucesso")

    return render(request, "alunos/cadastro_aluno.html", {"form": form})


def sucesso(request):
    return render(request, "alunos/sucesso.html")


# -------------------------
# ENSAIOS
# -------------------------

def ensaios_aluno(request):
    ensaios = EnsaiosproModel.objects.all()
    return render(request, "alunos/ensaios_aluno.html", {"ensaios": ensaios})


# -------------------------
# APRESENTAÇÕES
# -------------------------

def apresentacoes_aluno(request):
    apresentacoes = ApresentacaoModel.objects.all()
    return render(request, "alunos/apresentacoes_aluno.html", {"apresentacoes": apresentacoes})


# -------------------------
# MEU NAIPE (NOVO)
# -------------------------

@login_required
def meu_naipe(request):
    aluno = request.user.perfil.aluno  # aluno logado

    # Caso o aluno ainda não tenha naipe
    if not aluno.naipe:
        return render(request, "alunos/naipe_vazio.html")

    colegas = Aluno.objects.filter(naipe=aluno.naipe)

    return render(request, "alunos/meu_naipe.html", {
        "aluno": aluno,
        "naipe": aluno.naipe,
        "colegas": colegas,
    })


def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    form = AlunoForm(request.POST or None, instance=aluno)

    if form.is_valid():
        form.save()
        return redirect("contas:lista_alunos")

    return render(request, "alunos/editar_aluno.html", {"form": form, "aluno": aluno})

def excluir_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    perfil = aluno.perfil

    # Exclui o aluno e o perfil junto
    perfil.delete()

    return redirect("contas:lista_alunos")
