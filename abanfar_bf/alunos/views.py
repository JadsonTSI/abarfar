from django.shortcuts import render, redirect
from .forms import AlunoCadastroForm
from django import forms
from professores.models import EnsaiosproModel, ApresentacaoModel



def cadastrar_aluno(request):
    form = AlunoCadastroForm()

    if request.method == "POST":
        form = AlunoCadastroForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect("alunos:sucesso")
            except forms.ValidationError as e:
                form.add_error(None, e)

    return render(request, "alunos/cadastro_aluno.html", {"form": form})


def sucesso(request):
    return render(request, "alunos/sucesso.html")

# ver ensaios

def ensaios_aluno(request):
    ensaios = EnsaiosproModel.objects.all()
    return render(request, "alunos/ensaios_aluno.html", {"ensaios": ensaios})

# apresentação 

def apresentacoes_aluno(request):
    apresentacoes = ApresentacaoModel.objects.all()
    return render(request, "alunos/apresentacoes_aluno.html", {"apresentacoes": apresentacoes})
