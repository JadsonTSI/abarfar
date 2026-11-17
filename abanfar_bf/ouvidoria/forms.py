from django import forms

from .models import Manifestacao

OBRIGATORIO = "Este campo é obrigatório."


class ManifestacaoForm(forms.ModelForm):
    # Campo-armadilha contra robôs: fica escondido na página; pessoas não preenchem.
    site = forms.CharField(required=False)
    concordo = forms.BooleanField(
        error_messages={"required": "É preciso concordar para enviar a manifestação."},
    )

    class Meta:
        model = Manifestacao
        fields = ["tipo", "anonima", "nome", "email", "telefone", "assunto", "mensagem"]
        # O projeto usa LANGUAGE_CODE en-us: mensagens em português definidas aqui.
        error_messages = {
            "tipo": {"required": "Escolha o tipo de manifestação.", "invalid_choice": "Escolha um tipo válido."},
            "assunto": {"required": OBRIGATORIO, "max_length": "Assunto longo demais (máx. 150 caracteres)."},
            "mensagem": {"required": OBRIGATORIO},
            "email": {"invalid": "Informe um e-mail válido."},
            "nome": {"max_length": "Nome longo demais."},
            "telefone": {"max_length": "Telefone longo demais."},
        }

    def clean_site(self):
        if self.cleaned_data.get("site"):
            raise forms.ValidationError("Envio bloqueado.")
        return ""

    def clean(self):
        dados = super().clean()
        for campo in ("assunto", "mensagem", "nome", "telefone"):
            if isinstance(dados.get(campo), str):
                dados[campo] = dados[campo].strip()

        if "assunto" in dados and not dados["assunto"] and "assunto" not in self.errors:
            self.add_error("assunto", OBRIGATORIO)
        mensagem = dados.get("mensagem")
        if mensagem is not None and len(mensagem) < 10 and "mensagem" not in self.errors:
            self.add_error("mensagem", "Descreva sua manifestação com um pouco mais de detalhe.")

        if not dados.get("anonima"):
            if not dados.get("nome") and "nome" not in self.errors:
                self.add_error("nome", "Informe seu nome ou marque a opção de manifestação anônima.")
            if not dados.get("email") and "email" not in self.errors:
                self.add_error("email", "Informe um e-mail para receber a resposta, ou marque a opção anônima.")
        return dados


class AcompanharForm(forms.Form):
    protocolo = forms.CharField(
        max_length=20,
        error_messages={"required": "Informe o número do protocolo.", "max_length": "Protocolo inválido."},
    )

    def clean_protocolo(self):
        return self.cleaned_data["protocolo"].strip().upper()
