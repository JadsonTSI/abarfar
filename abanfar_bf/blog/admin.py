from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tag', 'data_publicacao', 'autor')
    prepopulated_fields = {'slug': ('titulo',)}
    search_fields = ('titulo', 'conteudo')
    list_filter = ('tag', 'data_publicacao')
