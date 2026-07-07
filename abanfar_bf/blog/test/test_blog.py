from django.test import TestCase
from django.urls import reverse
from transparencia.models import Documento
from blog.models import Post
from datetime import date

class BlogViewsTestCase(TestCase):
    def test_home_view(self):
        """Test if the homepage returns 200 OK and uses the correct template."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_post_detail_view(self):
        """Test if the post detail page returns 200 OK and renders correctly."""
        post = Post.objects.create(
            titulo="Trajetória de Teste",
            tag="Notícias",
            resumo="Um resumo de teste",
            conteudo="Conteúdo de teste",
            data_publicacao=date(2025, 5, 31)
        )
        response = self.client.get(reverse('post_detail', args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertContains(response, post.titulo)

    def test_portal_transparencia_view(self):
        """Test if the transparency portal returns 200 OK, uses the correct template, and handles query metrics."""
        # Create a sample Documento to test query and context calculations
        Documento.objects.create(
            titulo="Relatório Anual 2026",
            descricao="Descrição de teste",
            categoria="financeiro",
            ano=2026,
            arquivo="dummy.pdf",
            publicado=True
        )
        
        response = self.client.get(reverse('transparencia:portal'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/transparencia.html')
        self.assertIn('documentos', response.context)
        self.assertEqual(len(response.context['documentos']), 1)
        self.assertEqual(response.context['financeiro_count'], 1)

    def test_sobre_view(self):
        """Test if the sobre page returns 200 OK and uses the correct template."""
        response = self.client.get(reverse('sobre'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/sobre.html')

    def test_projetos_view(self):
        """Test if the projetos page returns 200 OK and uses the correct template."""
        response = self.client.get(reverse('projetos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/projetos.html')

    def test_galeria_view(self):
        """Test if the galeria page returns 200 OK and uses the correct template."""
        response = self.client.get(reverse('galeria'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/galeria.html')

    def test_contato_view_get(self):
        """Test if the contato page returns 200 OK and uses the correct template on GET request."""
        response = self.client.get(reverse('contato'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/contato.html')

    def test_contato_view_post(self):
        """Test if the contato page processes form submission correctly on POST request."""
        data = {
            'nome': 'João Silva',
            'email': 'joao@example.com',
            'assunto': 'Matrícula',
            'mensagem': 'Gostaria de matricular meu filho.'
        }
        response = self.client.post(reverse('contato'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/contato.html')
        # Check if success message is displayed
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn("Obrigado, João Silva!", str(messages[0]))

