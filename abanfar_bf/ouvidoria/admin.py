from django.contrib import admin
from django.utils import timezone

from .models import Manifestacao


@admin.register(Manifestacao)
class ManifestacaoAdmin(admin.ModelAdmin):
    list_display = ("protocolo", "tipo", "assunto", "quem", "status", "criada_em")
    list_filter = ("status", "tipo", "anonima", "criada_em")
    search_fields = ("protocolo", "assunto", "mensagem", "nome", "email")
    date_hierarchy = "criada_em"
    readonly_fields = ("protocolo", "tipo", "anonima", "nome", "email", "telefone",
                       "assunto", "mensagem", "criada_em", "atualizada_em", "respondida_em")
    fieldsets = (
        ("Manifestação", {"fields": ("protocolo", "tipo", "assunto", "mensagem", "criada_em")}),
        ("Manifestante", {"fields": ("anonima", "nome", "email", "telefone")}),
        ("Tratamento", {"fields": ("status", "resposta", "respondida_em", "observacoes_internas", "atualizada_em")}),
    )
    actions = ["marcar_em_analise", "marcar_encerrada"]

    @admin.display(description="Manifestante")
    def quem(self, obj):
        return "Anônimo" if obj.anonima else (obj.nome or "—")

    def has_add_permission(self, request):
        # As manifestações chegam pelo site; a equipe só faz o tratamento.
        return False

    def save_model(self, request, obj, form, change):
        if obj.resposta.strip() and not obj.respondida_em:
            obj.respondida_em = timezone.now()
            if obj.status in (Manifestacao.Status.RECEBIDA, Manifestacao.Status.EM_ANALISE):
                obj.status = Manifestacao.Status.RESPONDIDA
        super().save_model(request, obj, form, change)

    @admin.action(description="Marcar como em análise")
    def marcar_em_analise(self, request, queryset):
        queryset.filter(status=Manifestacao.Status.RECEBIDA).update(status=Manifestacao.Status.EM_ANALISE)

    @admin.action(description="Marcar como encerrada")
    def marcar_encerrada(self, request, queryset):
        queryset.update(status=Manifestacao.Status.ENCERRADA)
