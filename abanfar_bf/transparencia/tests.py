from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from contas.models import Perfil
from .models import Documento

class TransparenciaTestCase(TestCase):
    def setUp(self):
        # Create standard admin user
        self.gerente_user = User.objects.create_user(username="gerente", password="password123")
        self.gerente_perfil = Perfil.objects.create(user=self.gerente_user, tipo="gerente")
        
        # Create standard student user
        self.aluno_user = User.objects.create_user(username="aluno", password="password123")
        self.aluno_perfil = Perfil.objects.create(user=self.aluno_user, tipo="aluno")
        
        self.doc = Documento.objects.create(
            titulo="Relatório Financeiro Q1",
            descricao="Descrição Q1",
            categoria="financeiro",
            ano=2026,
            arquivo="q1.pdf",
            publicado=True
        )

    def test_portal_transparencia_public(self):
        response = self.client.get(reverse('transparencia:portal'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Relatório Financeiro Q1")

    def test_gestao_transparencia_anonymous_denied(self):
        response = self.client.get(reverse('transparencia:gestao'))
        self.assertRedirects(response, reverse('contas:login'))

    def test_gestao_transparencia_gerente_get(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('transparencia:gestao'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trasnparencia_gerente.html')

    def test_gestao_transparencia_create_success(self):
        self.client.login(username="gerente", password="password123")
        
        # Mocking pdf file upload
        pdf_file = SimpleUploadedFile("relatorio.pdf", b"pdf content", content_type="application/pdf")
        
        data = {
            'titulo': 'Relatório Novo',
            'descricao': 'Novo Doc',
            'categoria': 'atas',
            'ano': 2026,
            'publicado': True,
            'arquivo': pdf_file
        }
        response = self.client.post(reverse('transparencia:gestao'), data)
        self.assertRedirects(response, '/transparencia/gerente/?success=1')
        
        # Verify document was created
        new_doc = Documento.objects.get(titulo='Relatório Novo')
        self.assertEqual(new_doc.categoria, 'atas')
        self.assertEqual(new_doc.ano, 2026)
        
        # Clean up created file
        new_doc.arquivo.delete()

    def test_toggle_publicacao(self):
        self.client.login(username="gerente", password="password123")
        
        # Initial status is published (True)
        self.assertTrue(self.doc.publicado)
        
        response = self.client.post(reverse('transparencia:toggle', args=[self.doc.id]))
        self.assertRedirects(response, reverse('transparencia:gestao'))
        
        self.doc.refresh_from_db()
        self.assertFalse(self.doc.publicado)

    def test_excluir_documento(self):
        self.client.login(username="gerente", password="password123")
        
        response = self.client.post(reverse('transparencia:excluir', args=[self.doc.id]))
        self.assertRedirects(response, reverse('transparencia:gestao'))
        self.assertFalse(Documento.objects.filter(id=self.doc.id).exists())

    def test_gestao_transparencia_aluno_denied(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('transparencia:gestao'))
        self.assertRedirects(response, reverse('contas:login'))

        # Also post should be denied
        response_post = self.client.post(reverse('transparencia:gestao'), {})
        self.assertRedirects(response_post, reverse('contas:login'))

    def test_toggle_publicacao_aluno_denied(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.post(reverse('transparencia:toggle', args=[self.doc.id]))
        self.assertRedirects(response, reverse('contas:login'))
        
        # Doc should remain unchanged
        self.doc.refresh_from_db()
        self.assertTrue(self.doc.publicado)

    def test_excluir_documento_aluno_denied(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.post(reverse('transparencia:excluir', args=[self.doc.id]))
        self.assertRedirects(response, reverse('contas:login'))
        
        # Doc should still exist
        self.assertTrue(Documento.objects.filter(id=self.doc.id).exists())

    def test_gestao_transparencia_create_missing_fields_error(self):
        self.client.login(username="gerente", password="password123")
        # Submit with missing fields (no title, no file)
        data = {
            'titulo': '',
            'descricao': 'Sem titulo',
            'categoria': 'financeiro',
            'ano': 2026,
            'publicado': True
        }
        response = self.client.post(reverse('transparencia:gestao'), data)
        self.assertEqual(response.status_code, 200) # Re-renders the page
        # Check that no document was created
        self.assertEqual(Documento.objects.count(), 1) # Only the initial doc from setUp


