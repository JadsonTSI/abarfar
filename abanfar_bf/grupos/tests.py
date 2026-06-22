from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from contas.models import Perfil
from alunos.models import Aluno, GrupoMusical
from .models import Partitura

class GruposTestCase(TestCase):
    def setUp(self):
        # Create Professor
        self.prof_user = User.objects.create_user(username="prof", password="password123")
        self.prof_perfil = Perfil.objects.create(user=self.prof_user, tipo="professor")
        
        # Create Aluno
        self.aluno_user = User.objects.create_user(username="aluno", password="password123")
        self.aluno_perfil = Perfil.objects.create(user=self.aluno_user, tipo="aluno")
        
        self.grupo = GrupoMusical.objects.create(nome="Quinteto de Metais", descricao="Metais", ativo=True)
        self.aluno = Aluno.objects.create(perfil=self.aluno_perfil, nome="Carlos", sobrenome="Gomes", matricula="ALU6666", grupo=self.grupo)

    def test_lista_grupos(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('grupos:lista'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Quinteto de Metais")

    def test_grupo_detalhes_aluno(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('grupos:detalhes', args=[self.grupo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/detalhes_aluno.html')

    def test_grupo_detalhes_professor(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('grupos:detalhes', args=[self.grupo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grupos/detalhes.html')

    def test_enviar_partitura(self):
        self.client.login(username="prof", password="password123")
        pdf_file = SimpleUploadedFile("partitura.pdf", b"pdf content", content_type="application/pdf")
        
        data = {
            'titulo': 'Hino da ABANFAR',
            'arquivo': pdf_file
        }
        response = self.client.post(reverse('grupos:enviar_partitura', args=[self.grupo.id]), data)
        self.assertRedirects(response, reverse('grupos:detalhes', args=[self.grupo.id]))
        
        part = Partitura.objects.get(titulo='Hino da ABANFAR')
        self.assertEqual(part.grupo, self.grupo)
        part.arquivo.delete()

    def test_grupo_criar(self):
        self.client.login(username="prof", password="password123")
        data = {
            'nome': 'Banda Marcial',
            'descricao': 'Nova Banda',
            'ativo': True
        }
        response = self.client.post(reverse('grupos:criar'), data)
        self.assertRedirects(response, reverse('grupos:listar'))
        self.assertTrue(GrupoMusical.objects.filter(nome='Banda Marcial').exists())

    def test_grupo_editar(self):
        self.client.login(username="prof", password="password123")
        data = {
            'nome': 'Quinteto Editado',
            'descricao': 'Nova descrição',
            'ativo': True
        }
        response = self.client.post(reverse('grupos:editar', args=[self.grupo.id]), data)
        self.assertRedirects(response, reverse('grupos:listar'))
        
        self.grupo.refresh_from_db()
        self.assertEqual(self.grupo.nome, 'Quinteto Editado')

    def test_grupo_arquivar_and_reativar(self):
        self.client.login(username="prof", password="password123")
        
        # Archive
        response = self.client.post(reverse('grupos:arquivar', args=[self.grupo.id]))
        self.assertRedirects(response, reverse('grupos:listar'))
        self.grupo.refresh_from_db()
        self.assertFalse(self.grupo.ativo)
        
        # Re-activate
        response2 = self.client.post(reverse('grupos:reativar', args=[self.grupo.id]))
        self.assertRedirects(response2, reverse('grupos:listar'))
        self.grupo.refresh_from_db()
        self.assertTrue(self.grupo.ativo)

    def test_grupos_listar_dynamic_counts(self):
        from professores.models import EnsaiosproModel
        import datetime
        
        # In setUp: self.grupo is active, self.aluno is associated with it.
        # Let's create:
        # 1. Inactive group
        grupo_inativo = GrupoMusical.objects.create(nome="Grupo Inativo", descricao="Inativo", ativo=False)
        
        # 2. Student with no group
        aluno_sem_grupo_user = User.objects.create_user(username="aluno_sem", password="password123")
        aluno_sem_grupo_perfil = Perfil.objects.create(user=aluno_sem_grupo_user, tipo="aluno")
        Aluno.objects.create(perfil=aluno_sem_grupo_perfil, nome="Sem", sobrenome="Grupo", matricula="ALU7777")
        
        # 3. Upcoming rehearsal (today)
        EnsaiosproModel.objects.create(
            nome="Ensaio Quinteto",
            dia_semana="Sábado",
            data=datetime.date.today(),
            inicio=datetime.time(14, 0),
            fim=datetime.time(16, 0),
            local="Auditório",
            cancelado=False
        )
        
        # 4. Cancelled rehearsal (should be ignored)
        EnsaiosproModel.objects.create(
            nome="Ensaio Cancelado",
            dia_semana="Sábado",
            data=datetime.date.today(),
            inicio=datetime.time(16, 0),
            fim=datetime.time(18, 0),
            local="Auditório",
            cancelado=True
        )

        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('grupos:listar'))
        self.assertEqual(response.status_code, 200)
        
        # Total groups: self.grupo + grupo_inativo = 2
        self.assertEqual(response.context['grupos'].count(), 2)
        # Ativos: self.grupo = 1
        self.assertEqual(response.context['ativos_count'], 1)
        # Membros totais: self.aluno (has group). aluno_sem_grupo (has no group). Total: 1
        self.assertEqual(response.context['membros_totais_count'], 1)
        # Próximos ensaios: Ensaio Quinteto (active, today) = 1
        self.assertEqual(response.context['proximos_ensaios_count'], 1)

        # Check HTML renders correctly
        self.assertContains(response, "Total de grupos")
        self.assertContains(response, "Ativos")
        self.assertContains(response, "Membros totais")
        self.assertContains(response, "Próximos ensaios")

    def test_exportar_grupos_csv(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('grupos:exportar_grupos_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="grupos.csv"', response['Content-Disposition'])
        
        # Verify content
        content = response.content.decode('utf-8')
        self.assertIn('Quinteto de Metais', content)
        self.assertIn('Carlos Gomes', content)
        self.assertIn('Nome;Descricao;Ativo;Integrantes', content)

    def test_exportar_grupos_excel(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('grupos:exportar_grupos_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename="grupos.xlsx"', response['Content-Disposition'])

    def test_exportar_grupos_pdf(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('grupos:exportar_grupos_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="grupos.pdf"', response['Content-Disposition'])



