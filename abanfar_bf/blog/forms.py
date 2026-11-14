from django import forms
from .models import MensagemContato


class ContatoForm(forms.ModelForm):
    class Meta:
        model = MensagemContato
        fields = ["nome", "email", "assunto", "mensagem"]
        # O projeto usa LANGUAGE_CODE en-us: mensagens em português definidas aqui.
        error_messages = {
            campo: {
                "required": "Este campo é obrigatório.",
                "max_length": "Texto longo demais para este campo.",
            }
            for campo in fields
        }
        error_messages["email"]["invalid"] = "Informe um e-mail válido."

    def clean(self):
        dados = super().clean()
        for campo in ("nome", "assunto", "mensagem"):
            valor = (dados.get(campo) or "").strip()
            if campo in dados and not valor:
                self.add_error(campo, "Este campo é obrigatório.")
            elif valor:
                dados[campo] = valor
        return dados


class NewsletterForm(forms.Form):
    email = forms.EmailField(error_messages={
        "required": "Informe seu e-mail.",
        "invalid": "Informe um e-mail válido.",
    })
