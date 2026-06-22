from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Perfil
from alunos.models import Aluno

class ContasTestCase(TestCase):
    def setUp(self):
        # Create user accounts for testing
        self.gerente_user = User.objects.create_user(username="gerente", email="gerente@test.com", password="password123")
        self.gerente_perfil = Perfil.objects.create(user=self.gerente_user, tipo="gerente")
        
        self.aluno_user = User.objects.create_user(username="aluno", email="aluno@test.com", password="password123")
        self.aluno_perfil = Perfil.objects.create(user=self.aluno_user, tipo="aluno")
        self.aluno_obj = Aluno.objects.create(perfil=self.aluno_perfil, nome="Teste", sobrenome="Aluno", matricula="AL-999")

        self.professor_user = User.objects.create_user(username="professor", email="professor@test.com", password="password123")
        self.professor_perfil = Perfil.objects.create(user=self.professor_user, tipo="professor")

    def test_login_view_success_gerente(self):
        response = self.client.post(reverse('contas:login'), {
            'username': 'gerente',
            'senha': 'password123'
        })
        self.assertRedirects(response, reverse('contas:painel_gerente'))

    def test_login_view_success_aluno(self):
        response = self.client.post(reverse('contas:login'), {
            'username': 'aluno',
            'senha': 'password123'
        })
        self.assertRedirects(response, reverse('contas:painel_aluno'))

    def test_login_view_failed(self):
        response = self.client.post(reverse('contas:login'), {
            'username': 'gerente',
            'senha': 'wrongpassword'
        })
        self.assertRedirects(response, reverse('contas:login'))

    def test_logout_view(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('contas:logout'))
        self.assertRedirects(response, reverse('contas:login'))

    def test_painel_gerente_access_control(self):
        # Anonymous user should redirect to login
        response = self.client.get(reverse('contas:painel_gerente'))
        self.assertRedirects(response, reverse('contas:login'))

        # Aluno user should redirect to login
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('contas:painel_gerente'))
        self.assertRedirects(response, reverse('contas:login'))
        self.client.logout()

        # Gerente user should access 200 OK
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('contas:painel_gerente'))
        self.assertEqual(response.status_code, 200)

    def test_painel_aluno_access(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('contas:painel_aluno'))
        self.assertEqual(response.status_code, 200)

    def test_perfil_view_aluno(self):
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('contas:perfil'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['aluno'], self.aluno_obj)

    def test_alterar_foto(self):
        self.client.login(username="aluno", password="password123")
        
        # Mocking a simple image upload
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded_image = SimpleUploadedFile("avatar.gif", small_gif, content_type="image/gif")
        
        response = self.client.post(reverse('contas:alterar_foto'), {'foto': uploaded_image})
        self.assertRedirects(response, reverse('contas:perfil'))
        
        # Clean up files created
        self.aluno_perfil.refresh_from_db()
        self.assertTrue(self.aluno_perfil.foto.name.startswith('perfil_fotos/avatar'))
        self.aluno_perfil.foto.delete()

    def test_login_api_success(self):
        response = self.client.post(reverse('contas:login_api'), {
            'username': 'gerente',
            'senha': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['sucesso'])
        self.assertEqual(data['tipo'], 'gerente')

    def test_login_api_failed(self):
        response = self.client.post(reverse('contas:login_api'), {
            'username': 'gerente',
            'senha': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)
        data = response.json()
        self.assertIn('erro', data)

    def test_password_reset_flow_success(self):
        from django.core import mail
        # 1. Access reset form page
        response = self.client.get(reverse('contas:password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contas/password_reset_form.html')
        
        # 2. Submit e-mail
        response2 = self.client.post(reverse('contas:password_reset'), {'email': 'aluno@test.com'})
        self.assertRedirects(response2, reverse('contas:password_reset_done'))
        
        # 3. Check outbox
        self.assertEqual(len(mail.outbox), 1)
        email_sent = mail.outbox[0]
        self.assertEqual(email_sent.to, ['aluno@test.com'])
        self.assertIn('redefini', email_sent.body.lower())
        self.assertIn('senha', email_sent.body.lower())
        
        # 4. Get the reset confirm URL from body
        import re
        urls = re.findall(r'http://[^\s]+', email_sent.body)
        self.assertTrue(len(urls) > 0)
        confirm_url = urls[0]
        
        # Remove host part
        confirm_path = confirm_url.replace('http://testserver', '').strip()
        
        # 5. Access redefinition link
        response3 = self.client.get(confirm_path, follow=True)
        self.assertEqual(response3.status_code, 200)
        self.assertTemplateUsed(response3, 'contas/password_reset_confirm.html')
        
        # 6. Save new password
        post_path = response3.request['PATH_INFO']
        response4 = self.client.post(post_path, {
            'new_password1': 'novasenha1234',
            'new_password2': 'novasenha1234'
        })
        self.assertRedirects(response4, reverse('contas:password_reset_complete'))
        
        # 7. Check if login works with new password
        login_success = self.client.login(username="aluno", password="novasenha1234")
        self.assertTrue(login_success)

    def test_painel_professor_access_control(self):
        # Anonymous user should redirect to login
        response = self.client.get(reverse('contas:painel_professor'))
        self.assertRedirects(response, reverse('contas:login'))

        # Aluno user should redirect to login
        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('contas:painel_professor'))
        self.assertRedirects(response, reverse('contas:login'))
        self.client.logout()

        # Professor user should redirect to actual professor home page
        self.client.login(username="professor", password="password123")
        response = self.client.get(reverse('contas:painel_professor'))
        self.assertRedirects(response, reverse('professores:professoreshome'))
        
        # Follow the redirect to check that it renders fine
        response_follow = self.client.get(reverse('contas:painel_professor'), follow=True)
        self.assertEqual(response_follow.status_code, 200)
        self.client.logout()

    def test_painel_aluno_access_control_denied(self):
        # Anonymous user should redirect to login
        response = self.client.get(reverse('contas:painel_aluno'))
        self.assertRedirects(response, reverse('contas:login'))

        # Professor user should redirect to login
        self.client.login(username="professor", password="password123")
        response = self.client.get(reverse('contas:painel_aluno'))
        self.assertRedirects(response, reverse('contas:login'))
        self.client.logout()

    def test_decorators_user_no_perfil_exception(self):
        # Create a user with no Perfil object
        user_no_perfil = User.objects.create_user(username="noperfil", password="password123")
        self.client.login(username="noperfil", password="password123")

        # Accessing page with gerente_required decorator should redirect to login
        response = self.client.get(reverse('contas:painel_gerente'))
        self.assertRedirects(response, reverse('contas:login'))

        # Accessing page with professor_required decorator should redirect to login
        response2 = self.client.get(reverse('contas:painel_professor'))
        self.assertRedirects(response2, reverse('contas:login'))

        # Accessing page with aluno_required decorator should redirect to login
        response3 = self.client.get(reverse('contas:painel_aluno'))
        self.assertRedirects(response3, reverse('contas:login'))

    def test_lista_alunos_dynamic_counts(self):
        from instrumentos.models import Instrumento
        from django.utils import timezone
        import datetime

        self.client.login(username="gerente", password="password123")

        # Create an instrument
        inst = Instrumento.objects.create(nome="Flauta")

        # Create active and inactive students, with and without instruments
        # User 1: Active, joined this month, has instrument
        u1 = User.objects.create_user(username="student1", password="password123")
        p1 = Perfil.objects.create(user=u1, tipo="aluno")
        a1 = Aluno.objects.create(perfil=p1, nome="Student", sobrenome="One", matricula="AL-001", instrumento=inst)

        # User 2: Inactive, joined this month, no instrument
        u2 = User.objects.create_user(username="student2", password="password123")
        u2.is_active = False
        u2.save()
        p2 = Perfil.objects.create(user=u2, tipo="aluno")
        a2 = Aluno.objects.create(perfil=p2, nome="Student", sobrenome="Two", matricula="AL-002")

        # User 3: Active, joined long ago (outside the July-July cycle)
        hoje = timezone.now().date()
        if hoje.month >= 7:
            ano_inicio = hoje.year
        else:
            ano_inicio = hoje.year - 1
        
        date_joined_before_cycle = timezone.make_aware(datetime.datetime(ano_inicio - 1, 6, 1))
        u3 = User.objects.create_user(username="student3", password="password123")
        u3.date_joined = date_joined_before_cycle
        u3.save()
        p3 = Perfil.objects.create(user=u3, tipo="aluno")
        a3 = Aluno.objects.create(perfil=p3, nome="Student", sobrenome="Three", matricula="AL-003")

        response = self.client.get(reverse('contas:lista_alunos'))
        self.assertEqual(response.status_code, 200)

        # Verify dynamic calculations passed to context
        self.assertEqual(response.context['ativos_count'], 3)
        self.assertEqual(response.context['com_instrumento_count'], 1)
        self.assertEqual(response.context['novos_este_mes_count'], 3)
        
        # Verify rendered content (e.g., Ativos count, novos count, etc.)
        self.assertContains(response, 'Ativos')
        self.assertContains(response, 'Com instrumento')
        self.assertContains(response, 'Novos este ano letivo')

    def test_exportar_alunos_csv(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('contas:exportar_alunos_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="alunos.csv"', response['Content-Disposition'])
        
        # Verify content
        content = response.content.decode('utf-8')
        self.assertIn('Nome;Sobrenome;Matricula;Telefone;Instrumento;Naipe;Grupo;Status', content)
        self.assertIn('Teste;Aluno;AL-999', content)

    def test_exportar_alunos_excel(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('contas:exportar_alunos_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename="alunos.xlsx"', response['Content-Disposition'])

    def test_exportar_alunos_pdf(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('contas:exportar_alunos_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="alunos.pdf"', response['Content-Disposition'])


    def test_painel_gerente_search(self):
        self.client.login(username="gerente", password="password123")
        
        # Search for student "Teste"
        response = self.client.get(reverse('contas:painel_gerente') + "?busca=Teste")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['busca'], 'Teste')
        
        # Verify student is in search results
        alunos_found = response.context['resultados_busca']['alunos']
        self.assertTrue(any(a.nome == 'Teste' for a in alunos_found))
        
        # Verify HTML renders search results
        self.assertContains(response, 'Resultados da busca por "Teste"')
