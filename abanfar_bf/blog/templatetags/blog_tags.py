from django import template

register = template.Library()

MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]


@register.filter
def data_extenso(data):
    """31 de maio de 2025 — independente do LANGUAGE_CODE do projeto."""
    try:
        return f"{data.day} de {MESES[data.month - 1]} de {data.year}"
    except (AttributeError, IndexError, TypeError):
        return ""


@register.filter
def data_curta(data):
    """31 mai 2025"""
    try:
        return f"{data.day:02d} {MESES[data.month - 1][:3]} {data.year}"
    except (AttributeError, IndexError, TypeError):
        return ""
