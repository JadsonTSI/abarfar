from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from contas.models import Perfil
from alunos.models import Aluno, GrupoMusical, Naipe
from .models import EnsaiosproModel, ApresentacaoModel, ProfessorModel

class ProfessoresTestCase(TestCase):
    def setUp(self):
        # Create user / profiles
        self.prof_user = User.objects.create_user(username="prof", password="password123")
        self.prof_perfil = Perfil.objects.create(user=self.prof_user, tipo="professor")
        self.gerente_user = User.objects.create_user(username="gerente", password="password123")
        self.gerente_perfil = Perfil.objects.create(user=self.gerente_user, tipo="gerente")
        self.professor = ProfessorModel.objects.create(
            perfil=self.prof_perfil,
            nome="Augusto",
            email="augusto@music.com",
            telefone="112222222",
            instrumento="Piano"
        )
        
        self.grupo = GrupoMusical.objects.create(nome="Coral", active=True) if hasattr(GrupoMusical, 'active') else GrupoMusical.objects.create(nome="Coral")
        self.naipe = Naipe.objects.create(nome="Cordas")
        
        # Create objects
        self.ensaio = EnsaiosproModel.objects.create(
            nome="Ensaio Geral",
            dia_semana="Sábado",
            data=datetime.date(2026, 6, 20),
            inicio=datetime.time(14, 0),
            fim=datetime.time(16, 0),
            local="Auditório"
        )
        
        self.apresentacao = ApresentacaoModel.objects.create(
            titulo="Concerto de Inverno",
            descricao="Apresentação Anual",
            data=datetime.date(2026, 6, 25),
            horario="19:00",
            local="Teatro Municipal",
            grupo="Orquestra"
        )

    def test_professores_home(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('professores:professoreshome'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'professores/professores_home.html')

    def test_ensaios_list(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('professores:ensaios_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensaio Geral")

    def test_ensaios_create(self):
        self.client.login(username="prof", password="password123")
        data = {
            'nome': 'Ensaio Sopros',
            'dia_semana': 'Segunda-feira',
            'data': '2026-06-22',
            'inicio': '09:00',
            'fim': '11:00',
            'local': 'Sala 3'
        }
        response = self.client.post(reverse('professores:ensaios_create'), data)
        self.assertRedirects(response, reverse('professores:ensaios_list'))
        self.assertTrue(EnsaiosproModel.objects.filter(nome='Ensaio Sopros').exists())

    def test_ensaios_edit(self):
        self.client.login(username="prof", password="password123")
        data = {
            'nome': 'Ensaio Geral Editado',
            'dia_semana': 'Sábado',
            'data': '2026-06-20',
            'inicio': '14:00',
            'fim': '17:00',
            'local': 'Auditório Novo'
        }
        response = self.client.post(reverse('professores:ensaios_edit', args=[self.ensaio.id]), data)
        self.assertRedirects(response, reverse('professores:ensaios_list'))
        self.ensaio.refresh_from_db()
        self.assertEqual(self.ensaio.local, 'Auditório Novo')

    def test_ensaios_delete(self):
        self.client.login(username="prof", password="password123")
        response = self.client.post(reverse('professores:ensaios_delete', args=[self.ensaio.id]))
        self.assertRedirects(response, reverse('professores:ensaios_list'))
        self.assertFalse(EnsaiosproModel.objects.filter(id=self.ensaio.id).exists())

    def test_apresentacoes_list(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('professores:apresentacoes_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Concerto de Inverno")

    def test_apresentacoes_create(self):
        self.client.login(username="prof", password="password123")
        data = {
            'titulo': 'Concerto da Primavera',
            'descricao': 'Show ao ar livre',
            'data': '2026-09-22',
            'horario': '18:00',
            'local': 'Praça Central',
            'grupo': 'Banda'
        }
        response = self.client.post(reverse('professores:apresentacoes_create'), data)
        self.assertRedirects(response, reverse('professores:apresentacoes_list'))
        self.assertTrue(ApresentacaoModel.objects.filter(titulo='Concerto da Primavera').exists())

    def test_apresentacoes_edit(self):
        self.client.login(username="prof", password="password123")
        data = {
            'titulo': 'Concerto de Inverno Editado',
            'descricao': 'Nova descrição',
            'data': '2026-06-25',
            'horario': '19:30',
            'local': 'Teatro Municipal',
            'grupo': 'Orquestra Sinfônica'
        }
        response = self.client.post(reverse('professores:apresentacoes_edit', args=[self.apresentacao.id]), data)
        self.assertRedirects(response, reverse('professores:apresentacoes_list'))
        self.apresentacao.refresh_from_db()
        self.assertEqual(self.apresentacao.horario, '19:30')

    def test_apresentacoes_delete(self):
        self.client.login(username="prof", password="password123")
        response = self.client.post(reverse('professores:apresentacoes_delete', args=[self.apresentacao.id]))
        self.assertRedirects(response, reverse('professores:apresentacoes_list'))
        self.assertFalse(ApresentacaoModel.objects.filter(id=self.apresentacao.id).exists())

    def test_cancelar_and_restaurar_ensaio(self):
        self.client.login(username="prof", password="password123")
        # Cancel
        response = self.client.post(reverse('professores:cancelar_ensaio', args=[self.ensaio.id]))
        self.assertRedirects(response, reverse('professores:ensaios_professor'))
        self.ensaio.refresh_from_db()
        self.assertTrue(self.ensaio.cancelado)
        
        # Restore
        response2 = self.client.post(reverse('professores:restaurar_ensaio', args=[self.ensaio.id]))
        self.assertRedirects(response2, reverse('professores:ensaios_professor'))
        self.ensaio.refresh_from_db()
        self.assertFalse(self.ensaio.cancelado)

    def test_professores_list(self):
        from materias.models import Materia
        
        # In setUp: self.professor is active, teaches "Piano". Total active: 1. Instrument count: 1 ("Piano").
        # Let's create:
        # 1. Inactive professor
        u_inativo = User.objects.create_user(username="prof_inativo", password="password123")
        p_inativo = Perfil.objects.create(user=u_inativo, tipo="professor")
        ProfessorModel.objects.create(
            perfil=p_inativo,
            nome="Inativo",
            email="inativo@music.com",
            telefone="11111111",
            instrumento="Piano",
            ativo=False
        )

        # 2. Active professor with different instrument "Violino"
        u_active2 = User.objects.create_user(username="prof_active2", password="password123")
        p_active2 = Perfil.objects.create(user=u_active2, tipo="professor")
        ProfessorModel.objects.create(
            perfil=p_active2,
            nome="Violinista",
            email="violino@music.com",
            telefone="22222222",
            instrumento="Violino",
            ativo=True
        )

        # 3. Active professor with "Não definido" instrument (should be excluded from instrument count)
        u_active3 = User.objects.create_user(username="prof_active3", password="password123")
        p_active3 = Perfil.objects.create(user=u_active3, tipo="professor")
        ProfessorModel.objects.create(
            perfil=p_active3,
            nome="SemInstrumento",
            email="sem@music.com",
            telefone="33333333",
            instrumento="Não definido",
            ativo=True
        )

        # Let's create some Materia objects
        Materia.objects.create(nome="Teoria Musical 1", professor=self.professor)
        Materia.objects.create(nome="Prática de Conjunto 1", professor=self.professor)

        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('professores:professores_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Augusto")

        # Total active: self.professor (Piano) + Violinista (Violino) + SemInstrumento (Não definido) = 3
        self.assertEqual(response.context['ativos_count'], 3)
        # Instrumentos: "Piano" (from self.professor & prof_inativo), "Violino" (from Violinista). Total distinct valid: 2
        self.assertEqual(response.context['instrumentos_count'], 2)
        # Materias: Teoria Musical 1 + Prática de Conjunto 1 = 2
        self.assertEqual(response.context['materias_count'], 2)

        # Check that the stats values are rendered in the HTML response
        self.assertContains(response, "Ativos")
        self.assertContains(response, "Instrumentos")
        self.assertContains(response, "Matérias")

    def test_professores_create(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'usuario': 'novoprof',
            'nome': 'Novo Professor',
            'email': 'novoprof@music.com',
            'telefone': '117777777',
            'instrumento': 'Violoncelo',
            'ativo': True,
            'senha': 'senhafoguete123'
        }
        response = self.client.post(reverse('professores:professores_create'), data)
        self.assertRedirects(response, reverse('professores:professores_list'))
        self.assertTrue(ProfessorModel.objects.filter(nome='Novo Professor').exists())

    def test_professores_edit(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'nome': 'Augusto Alterado',
            'email': 'augusto@music.com',
            'telefone': '112222222',
            'instrumento': 'Piano de Cauda',
            'ativo': True
        }
        response = self.client.post(reverse('professores:professores_edit', args=[self.professor.id]), data)
        self.assertRedirects(response, reverse('professores:professores_list'))
        
        self.professor.refresh_from_db()
        self.assertEqual(self.professor.nome, 'Augusto Alterado')

    def test_professores_delete(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.post(reverse('professores:professores_delete', args=[self.professor.id]))
        self.assertRedirects(response, reverse('professores:professores_list'))
        self.assertFalse(ProfessorModel.objects.filter(id=self.professor.id).exists())

    def test_naipes_view(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('professores:naipes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cordas")

    def test_naipe_detalhe(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('professores:naipe_detalhe', args=["Cordas"]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'professores/naipe_detalhe.html')

    def test_api_listar_ensaios(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('professores:api_listar_ensaios'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], "Ensaio Geral")

    def test_exportar_professores_csv(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('professores:exportar_professores_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="professores.csv"', response['Content-Disposition'])
        
        # Verify content
        content = response.content.decode('utf-8')
        self.assertIn('Nome;Email;Telefone;Instrumento;Status', content)
        self.assertIn('Augusto;augusto@music.com;112222222;Piano;Ativo', content)

    def test_exportar_professores_excel(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('professores:exportar_professores_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename="professores.xlsx"', response['Content-Disposition'])

    def test_exportar_professores_pdf(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('professores:exportar_professores_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="professores.pdf"', response['Content-Disposition'])


