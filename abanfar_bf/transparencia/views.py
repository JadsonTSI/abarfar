from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from contas.decorators import gerente_required
from .models import Documento
 
# ── PÁGINA PÚBLICA DO BLOG ──────────────────────────────────
def portal_transparencia(request):
    """Página pública — qualquer visitante pode ver."""
    documentos = Documento.objects.filter(publicado=True)
 
    # Contagens por categoria
    context = {
        'documentos':          documentos,
        'anos':                documentos.values_list('ano', flat=True).distinct(),
        'atas_count':          documentos.filter(categoria='atas').count(),
        'financeiro_count':    documentos.filter(categoria='financeiro').count(),
        'institucional_count': documentos.filter(categoria='institucional').count(),
        'editais_count':       documentos.filter(categoria='editais').count(),
        'projetos_count':      documentos.filter(categoria='projetos').count(),
    }
    return render(request, 'blog/transparencia.html', context)
 
 
# ── PAINEL DO GERENTE ───────────────────────────────────────
@gerente_required
def gestao_transparencia(request):
    """Painel privado onde o gerente gerencia os documentos."""
    if request.method == 'POST':
        titulo     = request.POST.get('titulo', '').strip()
        descricao  = request.POST.get('descricao', '').strip()
        categoria  = request.POST.get('categoria', '')
        ano        = request.POST.get('ano', '')
        publicado  = 'publicado' in request.POST
        arquivo    = request.FILES.get('arquivo')
 
        if titulo and categoria and ano and arquivo:
            Documento.objects.create(
                titulo=titulo,
                descricao=descricao,
                categoria=categoria,
                ano=int(ano),
                publicado=publicado,
                arquivo=arquivo,
            )
            messages.success(request, 'Documento publicado com sucesso!')
            return redirect('/transparencia/gerente/?success=1')
        else:
            messages.error(request, 'Preencha todos os campos obrigatórios e selecione um arquivo.')
 
    documentos = Documento.objects.all()
 
    context = {
        'documentos':          documentos,
        'atas_count':          documentos.filter(categoria='atas').count(),
        'financeiro_count':    documentos.filter(categoria='financeiro').count(),
        'institucional_count': documentos.filter(categoria='institucional').count(),
        'editais_count':       documentos.filter(categoria='editais').count(),
        'projetos_count':      documentos.filter(categoria='projetos').count(),
    }
    return render(request, 'trasnparencia_gerente.html', context)
 
 
@gerente_required
def toggle_publicacao(request, doc_id):
    """Alterna entre publicado/rascunho."""
    doc = get_object_or_404(Documento, id=doc_id)
    doc.publicado = not doc.publicado
    doc.save()
    messages.success(request, f'{"Publicado" if doc.publicado else "Despublicado"}: {doc.titulo}')
    return redirect('transparencia:gestao')
 
 
@gerente_required
def excluir_documento(request, doc_id):
    """Exclui um documento."""
    doc = get_object_or_404(Documento, id=doc_id)
    doc.arquivo.delete(save=False)   # apaga o arquivo físico
    doc.delete()
    messages.success(request, 'Documento excluído.')
    return redirect('transparencia:gestao')