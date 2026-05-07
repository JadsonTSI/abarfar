from django.contrib import admin
from .models import Documento
 
@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display  = ['titulo', 'categoria', 'ano', 'publicado', 'data_publicacao']
    list_filter   = ['categoria', 'ano', 'publicado']
    search_fields = ['titulo', 'descricao']
    list_editable = ['publicado']
    ordering      = ['-ano', '-data_publicacao']
