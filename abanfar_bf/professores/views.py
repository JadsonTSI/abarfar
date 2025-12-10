from django.shortcuts import render, redirect, get_object_or_404
from .models import EnsaiosproModel, ApresentacaoModel, ProfessorModel
from .forms import EnsaiosForm, ApresentacaoForm, ProfessorForm, ProfessorEditForm
from django.http import HttpResponse
from alunos.models import Aluno, Naipe

# home

def professores_login(request):
    return HttpResponse("login dos professores")

def professores_home(request):
    return render(request, "professores/professores_home.html")


# Ensaios
# LISTAR
def ensaios_list(request):
    ensaios = EnsaiosproModel.objects.all()
    return render(request, "professores/ensaios_list.html", {"ensaios": ensaios})

# CRIAR
def ensaios_create(request):
    if request.method == "POST":
        form = EnsaiosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("professores:ensaios_list")
    else:
        form = EnsaiosForm()

    return render(request, "professores/ensaios_pro.html", {"form": form})

# EDITAR
def ensaios_edit(request, id):
    ensaio = get_object_or_404(EnsaiosproModel, id=id)
    
    if request.method == "POST":
        form = EnsaiosForm(request.POST, instance=ensaio)
        if form.is_valid():
            form.save()
            return redirect("professores:ensaios_list")
    else:
        form = EnsaiosForm(instance=ensaio)

    return render(request, "professores/ensaios_pro.html", {"form": form})

# EXCLUIR
def ensaios_delete(request, id):
    ensaio = get_object_or_404(EnsaiosproModel, id=id)

    if request.method == "POST":
        ensaio.delete()
        return redirect("professores:ensaios_list")

    return render(request, "professores/ensaios_confirm_delete.html", {"ensaio": ensaio})

# Apresentações

def apresentacoes_list(request):
    apresentacoes = ApresentacaoModel.objects.all()
    return render(request, "professores/apresentacoes_list.html", {"apresentacoes": apresentacoes})

# CRIAR
def apresentacoes_create(request):
    if request.method == "POST":
        form = ApresentacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("professores:apresentacoes_list")
    else:
        form = ApresentacaoForm()

    return render(request, "professores/apresentacoes_form.html", {"form": form})

# EDITAR
def apresentacoes_edit(request, id):
    apresentacao = get_object_or_404(ApresentacaoModel, id=id)

    if request.method == "POST":
        form = ApresentacaoForm(request.POST, instance=apresentacao)
        if form.is_valid():
            form.save()
            return redirect("professores:apresentacoes_list")
    else:
        form = ApresentacaoForm(instance=apresentacao)

    return render(request, "professores/apresentacoes_form.html", {"form": form})

# EXCLUIR
def apresentacoes_delete(request, id):
    apresentacao = get_object_or_404(ApresentacaoModel, id=id)

    if request.method == "POST":
        apresentacao.delete()
        return redirect("professores:apresentacoes_list")

    return render(request, "professores/apresentacoes_confirm_delete.html", {"apresentacao": apresentacao})

#cancelar


def lista_ensaios_professor(request):
    ensaios = EnsaiosproModel.objects.all()
    return render(request, "professores/ensaios_professor.html", {"ensaios": ensaios})


def cancelar_ensaio(request, id):
    ensaio = get_object_or_404(EnsaiosproModel, id=id)
    ensaio.cancelado = True
    ensaio.save()
    return redirect("professores:ensaios_professor")


def restaurar_ensaio(request, id):
    ensaio = get_object_or_404(EnsaiosproModel, id=id)
    ensaio.cancelado = False
    ensaio.save()
    return redirect("professores:ensaios_professor")


# cadastro professor

# LISTAR
def professores_list(request):
    professores = ProfessorModel.objects.all()
    return render(request, "professores/professores_list.html", {"professores": professores})

# CRIAR
def professores_create(request):
    if request.method == "POST":
        form = ProfessorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("professores:professores_list")
    else:
        form = ProfessorForm()

    return render(request, "professores/professores_form.html", {"form": form})


# EDITAR
def professores_edit(request, id):
    professor = get_object_or_404(ProfessorModel, id=id)

    if request.method == "POST":
        form = ProfessorEditForm(request.POST, instance=professor)
        if form.is_valid():
            form.save()
            return redirect("professores:professores_list")
    else:
        form = ProfessorEditForm(instance=professor)

    return render(request, "professores/professores_form.html", {"form": form})


# EXCLUIR
def professores_delete(request, id):
    professor = get_object_or_404(ProfessorModel, id=id)

    if request.method == "POST":
        professor.delete()
        return redirect("professores:professores_list")

    return render(request, "professores/professores_confirm_delete.html", {"professor": professor})


def naipes_view(request):
    naipes = Naipe.objects.all().order_by("nome")
    return render(request, "professores/naipes.html", {"naipes": naipes})


def naipe_detalhe(request, nome):
    naipe = get_object_or_404(Naipe, nome=nome)
    alunos = Aluno.objects.filter(naipe=naipe)

    return render(request, "professores/naipe_detalhe.html", {
        "naipe": naipe,
        "alunos": alunos
    })

