from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from contas.models import Perfil
from instrumentos.models import Instrumento
from alunos.models import Aluno, GrupoMusical, Naipe

class AlunosTestCase(TestCase):
    def setUp(self):
        # Create standard accounts
        self.aluno_user = User.objects.create_user(username="aluno", password="password123")
        self.aluno_perfil = Perfil.objects.create(user=self.aluno_user, tipo="aluno")
        self.gerente_user = User.objects.create_user(username="gerente", password="password123")
        self.gerente_perfil = Perfil.objects.create(user=self.gerente_user, tipo="gerente")
        
        self.grupo = GrupoMusical.objects.create(nome="Sinfônica", descricao="Banda Principal", ativo=True)
        self.naipe = Naipe.objects.create(nome="Metais")
        self.instrumento = Instrumento.objects.create(nome="Trompete", condicao="bom")
        
        self.aluno_obj = Aluno.objects.create(
            perfil=self.aluno_perfil,
            nome="Eduardo",
            sobrenome="Lima",
            matricula="ALU0001",
            telefone="11999999999",
            grupo=self.grupo,
            naipe=self.naipe,
            instrumento=self.instrumento
        )

    def test_cadastrar_aluno_view_get(self):
        response = self.client.get(reverse('alunos:cadastrar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alunos/cadastro_aluno.html')

    def test_cadastrar_aluno_view_post_success(self):
        # Instrument and group needed
        inst = Instrumento.objects.create(nome="Saxofone", condicao="otimo")
        
        data = {
            'nome': 'João',
            'sobrenome': 'Silva',
            'usuario': 'joaosilva',
            'email': 'joao@silva.com',
            'telefone': '1188888888',
            'senha': 'senhafoguete123',
            'grupo': self.grupo.id,
            'instrumento': inst.id,
            'naipe': 'Cordas'
        }
        response = self.client.post(reverse('alunos:cadastrar'), data)
        self.assertRedirects(response, reverse('alunos:sucesso'))
        self.assertTrue(User.objects.filter(username='joaosilva').exists())
        self.assertTrue(Aluno.objects.filter(nome='João').exists())

    def test_meu_naipe_view_with_naipe(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('alunos:meu_naipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alunos/meu_naipe.html')
        self.assertEqual(response.context['naipe'], self.naipe)

    def test_meu_naipe_view_without_naipe(self):
        # Create an aluno without a naipe
        user2 = User.objects.create_user(username="aluno2", password="password123")
        perfil2 = Perfil.objects.create(user=user2, tipo="aluno")
        Aluno.objects.create(
            perfil=perfil2,
            nome="Marcos",
            sobrenome="Gomes",
            matricula="ALU0002"
        )
        
        self.client.login(username="aluno2", password="password123")
        response = self.client.get(reverse('alunos:meu_naipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'alunos/naipe_vazio.html')

    def test_editar_aluno(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'nome': 'Eduardo Alterado',
            'sobrenome': 'Lima',
            'telefone': '11999999999',
            'grupo': self.grupo.id,
            'instrumento': self.instrumento.id,
            'naipe': self.naipe.id
        }
        response = self.client.post(reverse('alunos:editar', args=[self.aluno_obj.id]), data)
        self.assertRedirects(response, reverse('contas:lista_alunos'))
        
        self.aluno_obj.refresh_from_db()
        self.assertEqual(self.aluno_obj.nome, 'Eduardo Alterado')

    def test_excluir_aluno(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.post(reverse('alunos:excluir', args=[self.aluno_obj.id]))
        self.assertRedirects(response, reverse('contas:lista_alunos'))
        self.assertFalse(Aluno.objects.filter(id=self.aluno_obj.id).exists())

    def test_api_listar_alunos(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('alunos:api_listar_alunos'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], "Eduardo Lima")
