from django.shortcuts import render, redirect, get_object_or_404
from .models import Instrumento, InstrumentoEmprestimo
from .forms import InstrumentoForm, InstrumentoEmprestimoForm

# LISTAR INSTRUMENTOS
def list_instrumentos(request):
    instrumentos = Instrumento.objects.all()
    return render(request, "instrumentos/list.html", {"instrumentos": instrumentos})

# CADASTRAR INSTRUMENTO
def criar_instrumento(request):
    if request.method == "POST":
        form = InstrumentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("instrumentos:list")
    else:
        form = InstrumentoForm()

    return render(request, "instrumentos/form.html", {"form": form})

# ATRIBUIR / EMPRESTAR INSTRUMENTO
def atribuir_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)

    if request.method == "POST":
        form = InstrumentoEmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.instrumento = instrumento
            emprestimo.save()
            return redirect("instrumentos:list")
    else:
        form = InstrumentoEmprestimoForm()

    return render(request, "instrumentos/atribuir.html", {
        "form": form,
        "instrumento": instrumento
    })

# USO / HISTÓRICO DE EMPRESTIMOS
def uso_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    usos = InstrumentoEmprestimo.objects.filter(instrumento=instrumento)

    return render(request, "instrumentos/uso.html", {
        "instrumento": instrumento,
        "usos": usos
    })


def editar_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)
    
    if request.method == "POST":
        form = InstrumentoForm(request.POST, instance=instrumento)
        if form.is_valid():
            form.save()
            return redirect("instrumentos:list")
    else:
        form = InstrumentoForm(instance=instrumento)

    return render(request, "instrumentos/editar.html", {"form": form, "instrumento": instrumento})


def excluir_instrumento(request, id):
    instrumento = get_object_or_404(Instrumento, id=id)

    if request.method == "POST":
        instrumento.delete()
        return redirect("instrumentos:list")

    return render(request, "instrumentos/excluir.html", {"instrumento": instrumento})
