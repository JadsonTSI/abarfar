from django.contrib import admin
from .models import Instrumento, InstrumentoEmprestimo, IoTScan

@admin.register(Instrumento)
class InstrumentoAdmin(admin.ModelAdmin):
    list_display = ('identificador', 'nome', 'rfid', 'condicao', 'ativo', 'pertence_associacao')
    search_fields = ('identificador', 'nome', 'rfid')
    list_filter = ('condicao', 'ativo', 'pertence_associacao')

@admin.register(InstrumentoEmprestimo)
class InstrumentoEmprestimoAdmin(admin.ModelAdmin):
    list_display = ('instrumento', 'aluno', 'data_emprestimo', 'data_devolucao', 'devolvido')
    list_filter = ('devolvido', 'data_emprestimo', 'data_devolucao')
    search_fields = ('instrumento__nome', 'instrumento__identificador', 'aluno__nome', 'aluno__sobrenome', 'aluno__matricula')

@admin.register(IoTScan)
class IoTScanAdmin(admin.ModelAdmin):
    list_display = ('rfid', 'timestamp')
    search_fields = ('rfid',)
    list_filter = ('timestamp',)

