from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from contas.models import Perfil
from alunos.models import Aluno, GrupoMusical
from professores.models import ProfessorModel
from .models import Materia, MatriculaMateria

class MateriasTestCase(TestCase):
    def setUp(self):
        # Gerente account
        self.gerente_user = User.objects.create_user(username="gerente", password="password123")
        self.gerente_perfil = Perfil.objects.create(user=self.gerente_user, tipo="gerente")
        
        # Professor account
        self.prof_user = User.objects.create_user(username="prof", password="password123")
        self.prof_perfil = Perfil.objects.create(user=self.prof_user, tipo="professor")
        self.professor = ProfessorModel.objects.create(
            perfil=self.prof_perfil,
            nome="Augusto",
            email="augusto@music.com",
            telefone="112222222",
            instrumento="Piano"
        )
        
        # Aluno account
        self.grupo = GrupoMusical.objects.create(nome="Musicalização", ativo=True)
        self.aluno_user = User.objects.create_user(username="aluno", password="password123")
        self.aluno_perfil = Perfil.objects.create(user=self.aluno_user, tipo="aluno")
        self.aluno = Aluno.objects.create(perfil=self.aluno_perfil, nome="Paulo", sobrenome="Mendes", matricula="ALU5555", grupo=self.grupo)
        
        # Materia
        self.materia = Materia.objects.create(
            nome="Teoria Musical 1",
            professor=self.professor,
            google_classroom_link="http://class.google.com"
        )

    def test_lista_materias_gerente(self):
        # 1. Create inactive professor
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

        # 2. Create another active professor teaching Violino
        u_active2 = User.objects.create_user(username="prof_active2", password="password123")
        p_active2 = Perfil.objects.create(user=u_active2, tipo="professor")
        prof2 = ProfessorModel.objects.create(
            perfil=p_active2,
            nome="Violinista",
            email="violino@music.com",
            telefone="22222222",
            instrumento="Violino",
            ativo=True
        )

        # 3. Create another subject for prof2 (Violino)
        Materia.objects.create(nome="Prática de Violino", professor=prof2)

        # 4. Matriculate self.aluno to self.materia
        MatriculaMateria.objects.create(materia=self.materia, aluno=self.aluno)

        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('materias:materias_gerente'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teoria Musical 1")
        self.assertContains(response, "Prática de Violino")

        # Total active professors: self.professor (active) + prof2 (active) = 2 (inativo is inactive)
        self.assertEqual(response.context['professores_ativos_count'], 2)
        # Unique matriculated students: self.aluno = 1
        self.assertEqual(response.context['alunos_matriculados_count'], 1)
        # Unique instruments covered: self.professor (Piano) + prof2 (Violino) = 2
        self.assertEqual(response.context['instrumentos_cobertos_count'], 2)

        # Check HTML renders statistics labels
        self.assertContains(response, "Total de matérias")
        self.assertContains(response, "Professores ativos")
        self.assertContains(response, "Alunos matriculados")
        self.assertContains(response, "Instrumentos cobertos")

    def test_criar_materia(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'nome': 'Prática de Conjunto',
            'professor': self.professor.id
        }
        response = self.client.post(reverse('materias:criar_materia'), data)
        self.assertRedirects(response, reverse('materias:materias_gerente'))
        self.assertTrue(Materia.objects.filter(nome='Prática de Conjunto').exists())

    def test_matricular_alunos(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'aluno': self.aluno.id
        }
        response = self.client.post(reverse('materias:matricular_alunos', args=[self.materia.id]), data)
        self.assertRedirects(response, reverse('materias:materias_gerente'))
        self.assertTrue(MatriculaMateria.objects.filter(materia=self.materia, aluno=self.aluno).exists())

    def test_minhas_materias_professor(self):
        self.client.login(username="prof", password="password123")
        response = self.client.get(reverse('materias:materias_professor'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teoria Musical 1")

    def test_editar_link(self):
        self.client.login(username="prof", password="password123")
        data = {
            'link': 'http://classroom.google.com/newlink'
        }
        response = self.client.post(reverse('materias:editar_link', args=[self.materia.id]), data)
        self.assertRedirects(response, reverse('materias:materias_professor'))
        
        self.materia.refresh_from_db()
        self.assertEqual(self.materia.google_classroom_link, 'http://classroom.google.com/newlink')

    def test_materias_aluno(self):
        MatriculaMateria.objects.create(materia=self.materia, aluno=self.aluno)
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('materias:materias_aluno'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Teoria Musical 1")

    def test_editar_materia_get(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('materias:editar_materia', args=[self.materia.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'materias/gerente_editar.html')
        self.assertContains(response, "Teoria Musical 1")

    def test_editar_materia_post(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'nome': 'Teoria Musical Editada',
            'professor': self.professor.id,
            'google_classroom_link': 'http://classroom.google.com/newlink2'
        }
        response = self.client.post(reverse('materias:editar_materia', args=[self.materia.id]), data)
        self.assertRedirects(response, reverse('materias:materias_gerente'))
        
        self.materia.refresh_from_db()
        self.assertEqual(self.materia.nome, 'Teoria Musical Editada')
        self.assertEqual(self.materia.professor, self.professor)
        self.assertEqual(self.materia.google_classroom_link, 'http://classroom.google.com/newlink2')


