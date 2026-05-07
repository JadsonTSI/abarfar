from django.db import models
 
CATEGORIAS = [
    ('atas',          'Atas de Reunião'),
    ('financeiro',    'Relatório Financeiro'),
    ('institucional', 'Documento Institucional'),
    ('editais',       'Editais'),
    ('projetos',      'Projetos Musicais'),
    ('outros',        'Outros'),
]
 
class Documento(models.Model):
    titulo          = models.CharField(max_length=300, verbose_name='Título')
    descricao       = models.TextField(blank=True, null=True, verbose_name='Descrição')
    categoria       = models.CharField(max_length=30, choices=CATEGORIAS, verbose_name='Categoria')
    ano             = models.IntegerField(verbose_name='Ano de referência')
    arquivo         = models.FileField(upload_to='transparencia/', verbose_name='Arquivo')
    publicado       = models.BooleanField(default=True, verbose_name='Publicado')
    data_publicacao = models.DateField(auto_now_add=True, verbose_name='Data de publicação')
 
    class Meta:
        ordering = ['-ano', '-data_publicacao']
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
 
    def __str__(self):
        return f'{self.titulo} ({self.ano})'
