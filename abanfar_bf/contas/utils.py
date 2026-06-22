import os
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    """
    Renderiza um template HTML para PDF usando xhtml2pdf/pisa.
    Retorna um HttpResponse com o PDF ou None em caso de erro.
    """
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()

    def link_callback(uri, rel):
        """
        Converte URIs de static/media para caminhos absolutos no sistema de arquivos,
        necessário para que o xhtml2pdf possa carregar imagens e fontes corretamente.
        """
        from django.contrib.staticfiles import finders

        # Resolve arquivos estáticos
        if settings.STATIC_URL and uri.startswith(settings.STATIC_URL):
            uri_stripped = uri.replace(settings.STATIC_URL, "", 1)
            found = finders.find(uri_stripped)
            if found:
                return found

        # Resolve arquivos de mídia
        if settings.MEDIA_URL and uri.startswith(settings.MEDIA_URL):
            uri_stripped = uri.replace(settings.MEDIA_URL, "", 1)
            path = os.path.join(settings.MEDIA_ROOT, uri_stripped)
            if os.path.isfile(path):
                return path

        # Caminho direto no sistema de arquivos
        if os.path.isfile(uri):
            return uri

        # Fallback: tenta a partir do BASE_DIR
        fallback_path = os.path.join(settings.BASE_DIR, uri.lstrip('/'))
        if os.path.isfile(fallback_path):
            return fallback_path

        return uri

    pdf = pisa.pisaDocument(
        BytesIO(html.encode("utf-8")),
        result,
        encoding='utf-8',
        link_callback=link_callback,
    )

    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
