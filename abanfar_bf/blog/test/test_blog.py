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
        response = self.client.post(reverse('contato'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('contato'))
        self.assertTemplateUsed(response, 'blog/contato.html')
        # Check if success message is displayed
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertIn("Obrigado, João Silva!", str(messages[0]))



class MelhoriasSitePublicoTests(TestCase):
    def test_contato_salva_mensagem(self):
        from blog.models import MensagemContato
        self.client.post(reverse('contato'), {
            'nome': 'Ana', 'email': 'ana@example.com', 'assunto': 'Apoio', 'mensagem': 'Quero ajudar.'
        })
        msg = MensagemContato.objects.get()
        self.assertEqual(msg.nome, 'Ana')
        self.assertFalse(msg.lida)

    def test_contato_invalido_nao_salva_e_mostra_erros(self):
        from blog.models import MensagemContato
        response = self.client.post(reverse('contato'), {
            'nome': '   ', 'email': 'nao-e-email', 'assunto': 'X', 'mensagem': 'Oi'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(MensagemContato.objects.count(), 0)
        self.assertContains(response, 'field-error')
        # mantém o que a pessoa digitou
        self.assertContains(response, 'value="nao-e-email"')

    def test_newsletter_inscreve_uma_vez(self):
        from blog.models import InscricaoNewsletter
        url = reverse('newsletter')
        r1 = self.client.post(url, {'email': 'Fulano@Example.com', 'next': '/sobre/'})
        self.assertRedirects(r1, '/sobre/', fetch_redirect_response=False)
        self.client.post(url, {'email': 'fulano@example.com', 'next': '/'})
        self.assertEqual(InscricaoNewsletter.objects.count(), 1)
        self.assertEqual(InscricaoNewsletter.objects.get().email, 'fulano@example.com')

    def test_newsletter_ignora_redirect_externo(self):
        r = self.client.post(reverse('newsletter'), {'email': 'a@b.com', 'next': 'https://malicioso.example/'})
        self.assertRedirects(r, '/', fetch_redirect_response=False)

    def test_newsletter_so_aceita_post(self):
        self.assertEqual(self.client.get(reverse('newsletter')).status_code, 405)

    def test_lista_de_noticias_pagina(self):
        from datetime import date
        from blog.models import Post
        for i in range(8):
            Post.objects.create(titulo=f'Post {i}', tag='Notícias', resumo='r', conteudo='c', data_publicacao=date(2025, 1, i + 1))
        r1 = self.client.get(reverse('post_list'))
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(len(r1.context['posts']), 6)
        self.assertContains(r1, '?pagina=2')
        r2 = self.client.get(reverse('post_list') + '?pagina=2')
        self.assertEqual(len(r2.context['posts']), 2)
        # página inválida não quebra
        self.assertEqual(self.client.get(reverse('post_list') + '?pagina=abc').status_code, 200)

    def test_datas_em_portugues(self):
        from datetime import date
        from blog.models import Post
        post = Post.objects.create(titulo='Data teste', tag='Notícias', resumo='r', conteudo='c', data_publicacao=date(2025, 3, 7))
        r = self.client.get(reverse('post_detail', args=[post.slug]))
        self.assertContains(r, '7 de março de 2025')

    def test_home_sem_links_mortos(self):
        r = self.client.get(reverse('home'))
        self.assertNotContains(r, 'href="#"')

    def test_botao_painel_respeita_o_perfil(self):
        from django.contrib.auth.models import User
        from contas.models import Perfil
        user = User.objects.create_user('prof_teste', password='x')
        Perfil.objects.create(user=user, tipo='professor')
        self.client.force_login(user)
        r = self.client.get(reverse('home'))
        self.assertEqual(r.context['painel_url'], reverse('professores:professoreshome'))
        self.assertContains(r, 'Meu painel')
