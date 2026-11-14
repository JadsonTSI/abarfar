from django.contrib import admin
from .models import Post, MensagemContato, InscricaoNewsletter


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tag', 'data_publicacao', 'autor')
    prepopulated_fields = {'slug': ('titulo',)}
    search_fields = ('titulo', 'conteudo')
    list_filter = ('tag', 'data_publicacao')


@admin.register(MensagemContato)
class MensagemContatoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'assunto', 'criada_em', 'lida')
    list_filter = ('lida', 'criada_em')
    list_editable = ('lida',)
    search_fields = ('nome', 'email', 'assunto', 'mensagem')
    readonly_fields = ('nome', 'email', 'assunto', 'mensagem', 'criada_em')


@admin.register(InscricaoNewsletter)
class InscricaoNewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'criada_em')
    search_fields = ('email',)
