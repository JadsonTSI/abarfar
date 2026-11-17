import re

from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from ouvidoria.admin import ManifestacaoAdmin
from ouvidoria.models import Manifestacao

DADOS_VALIDOS = {
    "tipo": "sugestao",
    "nome": "Maria Souza",
    "email": "maria@example.com",
    "telefone": "84 99999-0000",
    "assunto": "Horário dos ensaios",
    "mensagem": "Sugiro ensaios também aos sábados pela manhã.",
    "concordo": "on",
}


class OuvidoriaPublicaTests(TestCase):
    def test_pagina_abre(self):
        r = self.client.get(reverse("ouvidoria:index"))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, "ouvidoria/ouvidoria.html")
        self.assertContains(r, "Registrar manifestação")

    def test_tipo_pre_selecionado_pela_url(self):
        r = self.client.get(reverse("ouvidoria:index") + "?tipo=elogio")
        self.assertContains(r, 'value="elogio" required\n                                               checked')

    def test_envio_valido_gera_protocolo_e_mostra_confirmacao(self):
        r = self.client.post(reverse("ouvidoria:index"), DADOS_VALIDOS, follow=True)
        self.assertRedirects(r, reverse("ouvidoria:enviada"))
        m = Manifestacao.objects.get()
        self.assertRegex(m.protocolo, r"^OUV-\d{4}-[A-Z2-9]{8}$")
        self.assertEqual(m.status, Manifestacao.Status.RECEBIDA)
        self.assertContains(r, m.protocolo)

    def test_protocolos_sao_unicos(self):
        protocolos = {Manifestacao.objects.create(tipo="elogio", assunto="a", mensagem="mensagem longa").protocolo for _ in range(20)}
        self.assertEqual(len(protocolos), 20)

    def test_anonima_nao_guarda_identificacao(self):
        dados = {**DADOS_VALIDOS, "tipo": "denuncia", "anonima": "on"}
        self.client.post(reverse("ouvidoria:index"), dados)
        m = Manifestacao.objects.get()
        self.assertTrue(m.anonima)
        self.assertEqual((m.nome, m.email, m.telefone), ("", "", ""))

    def test_anonima_dispensa_nome_e_email(self):
        dados = {k: v for k, v in DADOS_VALIDOS.items() if k not in ("nome", "email")}
        dados["anonima"] = "on"
        r = self.client.post(reverse("ouvidoria:index"), dados)
        self.assertEqual(r.status_code, 302)

    def test_identificada_exige_nome_e_email(self):
        dados = {k: v for k, v in DADOS_VALIDOS.items() if k not in ("nome", "email")}
        r = self.client.post(reverse("ouvidoria:index"), dados)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Manifestacao.objects.count(), 0)
        self.assertContains(r, "Informe seu nome")
        self.assertContains(r, "Informe um e-mail")

    def test_exige_tipo_relato_e_concordancia(self):
        r = self.client.post(reverse("ouvidoria:index"), {"nome": "A", "email": "a@b.com", "assunto": "x", "mensagem": "curto"})
        self.assertEqual(Manifestacao.objects.count(), 0)
        self.assertContains(r, "Escolha o tipo")
        self.assertContains(r, "mais de detalhe")
        self.assertContains(r, "É preciso concordar")

    def test_campo_armadilha_bloqueia_robo(self):
        r = self.client.post(reverse("ouvidoria:index"), {**DADOS_VALIDOS, "site": "http://spam.example"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Manifestacao.objects.count(), 0)

    def test_confirmacao_sem_envio_volta_para_formulario(self):
        r = self.client.get(reverse("ouvidoria:enviada"))
        self.assertRedirects(r, reverse("ouvidoria:index"))


class AcompanharTests(TestCase):
    def setUp(self):
        self.m = Manifestacao.objects.create(tipo="reclamacao", nome="João", email="j@example.com",
                                             assunto="Instrumento quebrado", mensagem="O trompete está com defeito.")

    def test_consulta_por_protocolo_minusculo_e_com_espacos(self):
        r = self.client.get(reverse("ouvidoria:acompanhar"), {"protocolo": f"  {self.m.protocolo.lower()} "})
        self.assertEqual(r.context["manifestacao"], self.m)
        self.assertContains(r, "Recebida")

    def test_protocolo_inexistente(self):
        r = self.client.get(reverse("ouvidoria:acompanhar"), {"protocolo": "OUV-2026-XXXXXXXX"})
        self.assertTrue(r.context["nao_encontrada"])
        self.assertContains(r, "Protocolo não encontrado")

    def test_mostra_resposta_mas_nao_observacoes_internas(self):
        self.m.resposta = "Trocamos o bocal do trompete."
        self.m.observacoes_internas = "NOTA-INTERNA-SECRETA"
        self.m.status = Manifestacao.Status.RESPONDIDA
        self.m.save()
        r = self.client.get(reverse("ouvidoria:acompanhar"), {"protocolo": self.m.protocolo})
        self.assertContains(r, "Trocamos o bocal do trompete.")
        self.assertNotContains(r, "NOTA-INTERNA-SECRETA")
        # dados pessoais do manifestante não aparecem na consulta pública
        self.assertNotContains(r, "j@example.com")

    def test_pagina_vazia(self):
        r = self.client.get(reverse("ouvidoria:acompanhar"))
        self.assertEqual(r.status_code, 200)
        self.assertIsNone(r.context["manifestacao"])


class AdminTests(TestCase):
    def test_responder_preenche_data_e_muda_situacao(self):
        m = Manifestacao.objects.create(tipo="sugestao", nome="A", email="a@b.com", assunto="x", mensagem="mensagem longa")
        admin = ManifestacaoAdmin(Manifestacao, AdminSite())
        request = RequestFactory().post("/")
        request.user = User.objects.create_superuser("adm", "adm@example.com", "x")
        m.resposta = "Obrigado pela sugestão!"
        admin.save_model(request, m, form=None, change=True)
        m.refresh_from_db()
        self.assertEqual(m.status, Manifestacao.Status.RESPONDIDA)
        self.assertIsNotNone(m.respondida_em)

    def test_menu_do_site_tem_ouvidoria(self):
        r = self.client.get(reverse("home"))
        self.assertTrue(re.search(r'href="/ouvidoria/"', r.content.decode()))
