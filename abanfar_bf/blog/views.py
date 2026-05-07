from django.shortcuts import render
from transparencia.models import Documento

def home(request):
    return render(request, "blog/home.html")

def portal_transparencia(request):
    from transparencia.models import Documento
 
    documentos = Documento.objects.filter(publicado=True)
 
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