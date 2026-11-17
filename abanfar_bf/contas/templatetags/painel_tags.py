from django import template

register = template.Library()

MESES_ABREV = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]


@register.filter
def mes_abrev(data):
    """Mês abreviado em português (ex.: 'Nov'), independente do LANGUAGE_CODE."""
    try:
        return MESES_ABREV[data.month - 1]
    except (AttributeError, IndexError, TypeError):
        return ""
