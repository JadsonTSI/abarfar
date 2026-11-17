from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import AcompanharForm, ManifestacaoForm
from .models import Manifestacao

SESSAO_PROTOCOLO = "ouvidoria_ultimo_protocolo"


def ouvidoria(request):
    if request.method == "POST":
        form = ManifestacaoForm(request.POST)
        if form.is_valid():
            manifestacao = form.save()
            # Guarda na sessão para a página de confirmação mostrar o protocolo
            request.session[SESSAO_PROTOCOLO] = manifestacao.protocolo
            return redirect("ouvidoria:enviada")
        messages.error(request, "Não foi possível registrar: confira os campos destacados.")
    else:
        tipo = request.GET.get("tipo")
        form = ManifestacaoForm(initial={"tipo": tipo} if tipo in Manifestacao.Tipo.values else None)
    return render(request, "ouvidoria/ouvidoria.html", {
        "form": form,
        "tipos": Manifestacao.Tipo,
    })


def enviada(request):
    protocolo = request.session.get(SESSAO_PROTOCOLO)
    manifestacao = Manifestacao.objects.filter(protocolo=protocolo).first() if protocolo else None
    if manifestacao is None:
        return redirect("ouvidoria:index")
    return render(request, "ouvidoria/enviada.html", {"manifestacao": manifestacao})


def acompanhar(request):
    form = AcompanharForm(request.GET or None)
    manifestacao = None
    nao_encontrada = False
    if form.is_bound and form.is_valid():
        manifestacao = Manifestacao.objects.filter(protocolo=form.cleaned_data["protocolo"]).first()
        nao_encontrada = manifestacao is None
    return render(request, "ouvidoria/acompanhar.html", {
        "form": form,
        "manifestacao": manifestacao,
        "nao_encontrada": nao_encontrada,
    })
