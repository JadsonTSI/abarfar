from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from alunos.models import GrupoMusical, Aluno
from .models import Partitura
from .forms import PartituraForm, GrupoForm


def editar_funcao(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)

    if request.method == "POST":
        aluno.funcao = request.POST.get("funcao")
        aluno.save()
        return redirect("grupos:detalhe_grupo", id=aluno.grupo.id)

    return render(request, "grupos/editar_funcao.html", {"aluno": aluno})


def grupo_detalhes(request, id):
    grupo = get_object_or_404(GrupoMusical, id=id)
    musicos = Aluno.objects.filter(grupo=grupo)
    partituras = grupo.partituras.all()

    contexto = {
        "grupo": grupo,
        "musicos": musicos,
        "partituras": partituras
    }

    return render(request, "grupos/detalhes.html", contexto)

@login_required
def enviar_partitura(request, id):
    grupo = get_object_or_404(GrupoMusical, id=id)

    if request.method == "POST":
        form = PartituraForm(request.POST, request.FILES)
        if form.is_valid():
            partitura = form.save(commit=False)
            partitura.grupo = grupo
            partitura.save()
            return redirect("grupos:detalhes", id=grupo.id)

    else:
        form = PartituraForm()

    return render(request, "grupos/enviar_partitura.html", {
        "form": form,
        "grupo": grupo
    })



def lista_grupos(request):
    grupos = GrupoMusical.objects.all()
    return render(request, "grupos/lista.html", {"grupos": grupos})

@login_required
def grupos_listar(request):
    grupos = GrupoMusical.objects.all()
    return render(request, "grupos/listar.html", {"grupos": grupos})


@login_required
def grupo_criar(request):
    if request.method == "POST":
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("grupos:listar")
    else:
        form = GrupoForm()

    return render(request, "grupos/criar.html", {"form": form})


@login_required
def grupo_editar(request, id):
    grupo = get_object_or_404(GrupoMusical, id=id)
    
    if request.method == "POST":
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            return redirect("grupos:listar")
    else:
        form = GrupoForm(instance=grupo)

    return render(request, "grupos/editar.html", {"form": form, "grupo": grupo})


@login_required
def grupo_arquivar(request, id):
    grupo = get_object_or_404(GrupoMusical, id=id)
    grupo.ativo = False
    grupo.save()
    return redirect("grupos:listar")


@login_required
def grupo_reativar(request, id):
    grupo = get_object_or_404(GrupoMusical, id=id)
    grupo.ativo = True
    grupo.save()
    return redirect("grupos:listar")
