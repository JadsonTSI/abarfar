from django.conf import settings
from django.urls import reverse

PAINEIS = {
    "gerente": "contas:painel_gerente",
    "professor": "professores:professoreshome",
    "aluno": "contas:painel_aluno",
}


def site(request):
    """Dados globais do site público: redes sociais e o painel certo para o usuário logado."""
    painel_url = None
    user = getattr(request, "user", None)
    if user is not None and user.is_authenticated:
        tipo = getattr(getattr(user, "perfil", None), "tipo", None)
        if tipo in PAINEIS:
            painel_url = reverse(PAINEIS[tipo])
        elif user.is_staff:
            painel_url = reverse("admin:index")

    redes = getattr(settings, "REDES_SOCIAIS", {}) or {}
    redes_sociais = [
        {"nome": nome, "icone": icone, "url": redes[chave]}
        for chave, nome, icone in (
            ("instagram", "Instagram", "bi-instagram"),
            ("facebook", "Facebook", "bi-facebook"),
            ("youtube", "YouTube", "bi-youtube"),
        )
        if redes.get(chave)
    ]
    return {"painel_url": painel_url, "redes_sociais": redes_sociais}
