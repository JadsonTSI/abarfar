from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from contas.models import Perfil
from alunos.models import Aluno, GrupoMusical
from .models import Instrumento, InstrumentoEmprestimo, IoTScan

class InstrumentosTestCase(TestCase):
    def setUp(self):
        self.gerente_user = User.objects.create_user(username="gerente", password="password123")
        self.gerente_perfil = Perfil.objects.create(user=self.gerente_user, tipo="gerente")
        
        self.grupo = GrupoMusical.objects.create(nome="Musicalização", ativo=True)
        self.aluno_user = User.objects.create_user(username="aluno", password="password123")
        self.aluno_perfil = Perfil.objects.create(user=self.aluno_user, tipo="aluno")
        self.aluno = Aluno.objects.create(perfil=self.aluno_perfil, nome="Carlos", sobrenome="Moura", matricula="ALU7777", grupo=self.grupo)
        
        self.instrumento = Instrumento.objects.create(
            nome="Flauta Transversal",
            condicao="otimo",
            rfid="TAG12345"
        )

    def test_list_instrumentos(self):
        # 1. Create inactive instrument (associacao)
        Instrumento.objects.create(
            nome="Instrumento Inativo",
            condicao="bom",
            rfid="TAG_INACTIVE",
            ativo=False
        )
        # 2. Create student instrument (active)
        Instrumento.objects.create(
            nome="Instrumento Aluno",
            condicao="bom",
            rfid="TAG_ALUNO",
            pertence_associacao=False,
            ativo=True
        )

        self.client.login(username="aluno", password="password123")
        response = self.client.get(reverse('instrumentos:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flauta Transversal")

        # Total instruments in database = 3
        # active count = self.instrumento + student instrument = 2
        # association count = self.instrumento + inactive instrument = 2
        # student count = student instrument = 1
        self.assertEqual(response.context['ativos_count'], 2)
        self.assertEqual(response.context['da_associacao_count'], 2)
        self.assertEqual(response.context['dos_alunos_count'], 1)

        # Check HTML renders statistics labels
        self.assertContains(response, "Total")
        self.assertContains(response, "Ativos")
        self.assertContains(response, "Da associação")
        self.assertContains(response, "Dos alunos")

    def test_criar_instrumento(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'nome': 'Clarinete',
            'condicao': 'bom',
            'pertence_associacao': True,
            'ativo': True,
            'rfid': 'TAG999'
        }
        response = self.client.post(reverse('instrumentos:create'), data)
        self.assertRedirects(response, reverse('instrumentos:list'))
        self.assertTrue(Instrumento.objects.filter(nome='Clarinete').exists())
        clarinete = Instrumento.objects.get(nome='Clarinete')
        self.assertEqual(clarinete.identificador, "INS-0002")

    def test_atribuir_instrumento(self):
        self.client.login(username="gerente", password="password123")
        data = {
            'aluno': self.aluno.id,
            'data_emprestimo': '2026-06-18',
            'observacao': 'Empréstimo de teste'
        }
        response = self.client.post(reverse('instrumentos:atribuir', args=[self.instrumento.id]), data)
        self.assertRedirects(response, reverse('instrumentos:list'))
        self.assertTrue(InstrumentoEmprestimo.objects.filter(instrumento=self.instrumento, aluno=self.aluno).exists())

    def test_uso_instrumento(self):
        self.client.login(username="aluno", password="password123")
        # Create loan
        InstrumentoEmprestimo.objects.create(instrumento=self.instrumento, aluno=self.aluno, devolvido=False)
        response = self.client.get(reverse('instrumentos:uso', args=[self.instrumento.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'instrumentos/uso.html')

    def test_api_painel_geral(self):
        response = self.client.get(reverse('instrumentos:api_painel'), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['instrumentos']['total'], 1)

    def test_api_buscar_rfid(self):
        response = self.client.get(reverse('instrumentos:api_buscar_rfid', args=["TAG12345"]), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['nome'], "Flauta Transversal")

    def test_api_registrar_retirada_and_devolucao(self):
        # Test withdrawal
        response = self.client.post(reverse('instrumentos:api_retirada'), {
            'rfid': 'TAG12345',
            'aluno_id': self.aluno.id
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['sucesso'])
        
        # Test withdrawal double-book error
        response2 = self.client.post(reverse('instrumentos:api_retirada'), {
            'rfid': 'TAG12345',
            'aluno_id': self.aluno.id
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response2.status_code, 400)
        
        # Test return (devolução)
        response3 = self.client.post(reverse('instrumentos:api_devolucao'), {
            'rfid': 'TAG12345'
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response3.status_code, 200)
        self.assertTrue(response3.json()['sucesso'])

    def test_api_iot_scan(self):
        response = self.client.post(reverse('instrumentos:api_iot_scan'), {
            'rfid': 'TAG_SCAN_1'
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['sucesso'])
        self.assertTrue(IoTScan.objects.filter(rfid='TAG_SCAN_1').exists())

    def test_api_iot_vincular_and_desvincular(self):
        # Bind new tag
        response = self.client.post(reverse('instrumentos:api_iot_vincular'), {
            'rfid': 'NEW_TAG_888',
            'instrumento_id': self.instrumento.id
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['sucesso'])
        
        self.instrumento.refresh_from_db()
        self.assertEqual(self.instrumento.rfid, 'NEW_TAG_888')
        
        # Unbind
        response2 = self.client.post(reverse('instrumentos:api_iot_desvincular'), {
            'instrumento_id': self.instrumento.id
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.json()['sucesso'])
        
        self.instrumento.refresh_from_db()
        self.assertIsNone(self.instrumento.rfid)

    def test_api_listar_instrumentos(self):
        response = self.client.get(reverse('instrumentos:api_listar'), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], "Flauta Transversal")

    def test_api_listar_emprestimos(self):
        # Create a loan
        InstrumentoEmprestimo.objects.create(instrumento=self.instrumento, aluno=self.aluno, devolvido=False)
        response = self.client.get(reverse('instrumentos:api_emprestimos'), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['instrumento'], "Flauta Transversal")
        self.assertEqual(data[0]['aluno'], "Carlos Moura")

    def test_api_iot_ultimo_scan(self):
        # 1. Test when there is no scan
        response1 = self.client.get(reverse('instrumentos:api_iot_ultimo_scan'), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response1.status_code, 200)
        self.assertIsNone(response1.json()['rfid'])

        # 2. Register a scan and test again
        IoTScan.objects.create(rfid="TAG12345")
        response2 = self.client.get(reverse('instrumentos:api_iot_ultimo_scan'), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response2.status_code, 200)
        data = response2.json()
        self.assertEqual(data['rfid'], "TAG12345")
        self.assertTrue(data['vinculado'])
        self.assertEqual(data['instrumento']['nome'], "Flauta Transversal")

    def test_api_instrumentos_sem_rfid(self):
        # Flauta has RFID (TAG12345). Create another instrument without RFID
        Instrumento.objects.create(nome="Saxofone Sem Tag", condicao="bom", rfid="")
        response = self.client.get(reverse('instrumentos:api_instrumentos_sem_rfid'), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['nome'], "Saxofone Sem Tag")

    def test_iot_web_control(self):
        # Must be logged in as gerente
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('instrumentos:iot_web_control'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "instrumentos/iot_control.html")

    def test_api_key_auth_failures_and_fallbacks(self):
        # 1. Missing API Key header
        response1 = self.client.get(reverse('instrumentos:api_listar'))
        self.assertEqual(response1.status_code, 401)
        
        # 2. Incorrect API Key header
        response2 = self.client.get(reverse('instrumentos:api_listar'), HTTP_X_API_KEY="wrong-token")
        self.assertEqual(response2.status_code, 401)

        # 3. Fallback: API Key in GET parameters
        response3 = self.client.get(reverse('instrumentos:api_listar') + "?api_key=abanfar-iot-secret-token-2026")
        self.assertEqual(response3.status_code, 200)

        # 4. Fallback: API Key in POST parameters (FormData)
        response4 = self.client.post(reverse('instrumentos:api_iot_scan'), {
            'rfid': 'TAG_SCAN_1',
            'api_key': 'abanfar-iot-secret-token-2026'
        })
        self.assertEqual(response4.status_code, 200)

        # 5. Fallback: API Key in POST JSON body
        import json
        response5 = self.client.post(
            reverse('instrumentos:api_iot_scan'),
            json.dumps({'rfid': 'TAG_SCAN_2', 'api_key': 'abanfar-iot-secret-token-2026'}),
            content_type='application/json'
        )
        self.assertEqual(response5.status_code, 200)

    def test_json_payload_parsing(self):
        import json
        # 1. Registrar Retirada via JSON
        data_retirada = {
            'rfid': 'TAG12345',
            'aluno_id': self.aluno.id
        }
        response1 = self.client.post(
            reverse('instrumentos:api_retirada'),
            json.dumps(data_retirada),
            content_type='application/json',
            HTTP_X_API_KEY="abanfar-iot-secret-token-2026"
        )
        self.assertEqual(response1.status_code, 200)
        self.assertTrue(response1.json()['sucesso'])

        # 2. Registrar Devolução via JSON
        data_devolucao = {
            'rfid': 'TAG12345'
        }
        response2 = self.client.post(
            reverse('instrumentos:api_devolucao'),
            json.dumps(data_devolucao),
            content_type='application/json',
            HTTP_X_API_KEY="abanfar-iot-secret-token-2026"
        )
        self.assertEqual(response2.status_code, 200)
        self.assertTrue(response2.json()['sucesso'])

    def test_iot_endpoints_error_scenarios(self):
        # 1. Non-existent Aluno ID in withdrawal
        response1 = self.client.post(reverse('instrumentos:api_retirada'), {
            'rfid': 'TAG12345',
            'aluno_id': 99999
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response1.status_code, 404)
        self.assertIn("Aluno nao encontrado", response1.json()['erro'])

        # 2. Non-existent Instrument RFID in withdrawal
        response2 = self.client.post(reverse('instrumentos:api_retirada'), {
            'rfid': 'NON_EXISTENT_TAG',
            'aluno_id': self.aluno.id
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response2.status_code, 404)
        self.assertIn("Instrumento com esta tag nao cadastrado", response2.json()['erro'])

        # 3. Non-existent Instrument RFID in return (devolução)
        response3 = self.client.post(reverse('instrumentos:api_devolucao'), {
            'rfid': 'NON_EXISTENT_TAG'
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response3.status_code, 404)
        self.assertIn("Instrumento nao cadastrado", response3.json()['erro'])

        # 4. Return request when no loan is active for this instrument
        response4 = self.client.post(reverse('instrumentos:api_devolucao'), {
            'rfid': 'TAG12345'
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response4.status_code, 404)
        self.assertIn("Nenhum emprestimo ativo", response4.json()['erro'])

        # 5. Binding a tag that is already bound to another instrument
        inst2 = Instrumento.objects.create(nome="Trombone", condicao="bom", rfid="TAG_EM_USO")
        # try to bind TAG_EM_USO to self.instrumento (which has id self.instrumento.id)
        response5 = self.client.post(reverse('instrumentos:api_iot_vincular'), {
            'rfid': 'TAG_EM_USO',
            'instrumento_id': self.instrumento.id
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response5.status_code, 400)
        self.assertIn("Tag ja esta em uso", response5.json()['erro'])

        # 6. Binding non-existent instrument
        response6 = self.client.post(reverse('instrumentos:api_iot_vincular'), {
            'rfid': 'NEW_TAG_ABC',
            'instrumento_id': 99999
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response6.status_code, 404)
        self.assertIn("Instrumento nao encontrado", response6.json()['erro'])

        # 7. Unbinding with missing parameters
        response7 = self.client.post(reverse('instrumentos:api_iot_desvincular'), {}, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response7.status_code, 400)
        self.assertIn("Informe rfid ou instrumento_id", response7.json()['erro'])

        # 8. Unbinding non-existent instrument
        response8 = self.client.post(reverse('instrumentos:api_iot_desvincular'), {
            'instrumento_id': 99999
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response8.status_code, 404)
        self.assertIn("Instrumento nao encontrado", response8.json()['erro'])

        # 9. Register scan with missing rfid
        response9 = self.client.post(reverse('instrumentos:api_iot_scan'), {}, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response9.status_code, 400)
        self.assertIn("rfid nao fornecido", response9.json()['erro'])

        # 10. Wrong HTTP method on POST-only endpoint (GET on withdraw API)
        response10 = self.client.get(reverse('instrumentos:api_retirada'), HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response10.status_code, 405)
        self.assertIn("Metodo nao permitido", response10.json()['erro'])

    def test_iot_scan_cleanup_limit(self):
        # Register 55 scans
        for i in range(55):
            IoTScan.objects.create(rfid=f"TAG_LIMIT_{i}")
            
        # Registering one more scan through API should trigger cleanup of old ones keeping only 50
        response = self.client.post(reverse('instrumentos:api_iot_scan'), {
            'rfid': 'TAG_TRIGGER'
        }, HTTP_X_API_KEY="abanfar-iot-secret-token-2026")
        self.assertEqual(response.status_code, 200)
        
        # Total scans should be exactly 50 (49 of the TAG_LIMIT_* plus TAG_TRIGGER)
        self.assertEqual(IoTScan.objects.count(), 50)
        # TAG_LIMIT_0 and TAG_LIMIT_1 should have been cleaned up
        self.assertFalse(IoTScan.objects.filter(rfid="TAG_LIMIT_0").exists())
        self.assertTrue(IoTScan.objects.filter(rfid="TAG_LIMIT_54").exists())

    def test_exportar_instrumentos_csv(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('instrumentos:exportar_instrumentos_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment; filename="instrumentos.csv"', response['Content-Disposition'])
        
        # Verify content
        content = response.content.decode('utf-8')
        self.assertIn('Flauta Transversal', content)
        self.assertIn('TAG12345', content)
        self.assertIn('Nome;Identificador;Descricao;Pertence a Associacao;Ativo;RFID;Condicao', content)

    def test_exportar_instrumentos_excel(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('instrumentos:exportar_instrumentos_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('attachment; filename="instrumentos.xlsx"', response['Content-Disposition'])

    def test_exportar_instrumentos_pdf(self):
        self.client.login(username="gerente", password="password123")
        response = self.client.get(reverse('instrumentos:exportar_instrumentos_pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment; filename="instrumentos.pdf"', response['Content-Disposition'])




