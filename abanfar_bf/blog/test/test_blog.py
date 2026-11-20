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


class LgpdETransparenciaTests(TestCase):
    def test_politica_de_privacidade(self):
        r = self.client.get(reverse('privacidade'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Lei nº 13.709/2018')
        self.assertContains(r, 'Crianças e adolescentes')

    def test_link_da_politica_em_todas_as_paginas(self):
        for nome in ('home', 'contato', 'sobre'):
            self.assertContains(self.client.get(reverse(nome)), reverse('privacidade'))

    def test_cancelar_newsletter(self):
        from blog.models import InscricaoNewsletter
        InscricaoNewsletter.objects.create(email='sair@example.com')
        r = self.client.post(reverse('newsletter_cancelar'), {'email': 'SAIR@example.com'}, follow=True)
        self.assertEqual(InscricaoNewsletter.objects.count(), 0)
        self.assertContains(r, 'removido da newsletter')
        # e-mail que não existe recebe a mesma resposta (não revela quem é inscrito)
        r2 = self.client.post(reverse('newsletter_cancelar'), {'email': 'nunca@example.com'}, follow=True)
        self.assertContains(r2, 'removido da newsletter')

    def test_mapa_do_google_so_carrega_com_clique(self):
        r = self.client.get(reverse('contato'))
        self.assertNotContains(r, '<iframe src="https://www.google.com/maps')
        self.assertContains(r, 'Carregar mapa')

    def test_programas_do_rodape_levam_a_secao_certa(self):
        html = self.client.get(reverse('home')).content.decode()
        projetos = self.client.get(reverse('projetos')).content.decode()
        for ancora in ('educacao-musical', 'orquestra-doce-som', 'banda-francisco-magalhaes', 'orquestra-filarmonica'):
            self.assertIn(f'/projetos/#{ancora}', html)
            self.assertIn(f'id="{ancora}"', projetos)
        self.assertNotIn('Ensino de Teoria Musical', html)

    def test_transparencia_vazia_explica_o_que_sera_publicado(self):
        r = self.client.get(reverse('transparencia:portal'))
        self.assertContains(r, 'Documentos em fase de publicação')
        self.assertNotContains(r, 'assim que o gerente os cadastrar')

    def test_dados_institucionais_so_aparecem_quando_preenchidos(self):
        from django.test import override_settings
        from django.conf import settings
        r = self.client.get(reverse('home'))
        self.assertNotContains(r, 'CNPJ')
        self.assertNotContains(r, 'wa.me')
        org = dict(settings.ORGANIZACAO, cnpj='12.345.678/0001-90', whatsapp='5584999990000')
        with override_settings(ORGANIZACAO=org):
            r = self.client.get(reverse('home'))
            self.assertContains(r, 'CNPJ 12.345.678/0001-90')
            self.assertContains(r, 'https://wa.me/5584999990000')


class HistoriaOficialTests(TestCase):
    def test_numeros_iguais_na_home_e_no_sobre(self):
        from django.conf import settings
        home = self.client.get(reverse('home')).content.decode()
        sobre = self.client.get(reverse('sobre')).content.decode()
        for n in settings.NUMEROS_INSTITUCIONAIS:
            self.assertIn(n['rotulo'], home)
            self.assertIn(n['rotulo'], sobre)
        for antigo in ('500+', '150+', '100+', 'Alunos formados'):
            self.assertNotIn(antigo, home + sobre)

    def test_linha_do_tempo_com_marcos_oficiais(self):
        sobre = self.client.get(reverse('sobre')).content.decode()
        for marco in ('2000–2001', 'Banda Renascer', '1º de novembro', '6 de janeiro', 'Copa dos Campeões', 'Orquestra Doce Som', '1º de julho'):
            self.assertIn(marco, sobre)

    def test_nomes_oficiais_dos_grupos(self):
        projetos = self.client.get(reverse('projetos')).content.decode()
        self.assertIn('Orquestra Doce Som', projetos)
        self.assertIn('todos os níveis', projetos)
        self.assertNotIn('Orquestra de Flautas', projetos)
        self.assertNotIn('banca interna', projetos)


class RefinoDesignTests(TestCase):
    def test_depoimentos_so_aparecem_quando_configurados(self):
        from django.conf import settings
        from django.test import override_settings
        r = self.client.get(reverse('home'))
        self.assertNotContains(r, 'O que dizem sobre nós')
        self.assertNotContains(r, 'Maria das Graças')
        dep = [{'nome': 'Pessoa Real', 'papel': 'Mãe de aluno', 'texto': 'Depoimento autorizado.'}]
        with override_settings(DEPOIMENTOS=dep):
            r = self.client.get(reverse('home'))
            self.assertContains(r, 'O que dizem sobre nós')
            self.assertContains(r, 'Depoimento autorizado.')

    def test_galeria_tem_lightbox_e_home_nao_tem_quadro_vazio(self):
        self.assertContains(self.client.get(reverse('galeria')), 'id="lightbox"')
        home = self.client.get(reverse('home'))
        self.assertContains(home, 'Ver galeria completa')
        self.assertNotContains(home, 'Festival de encerramento')
