from django import forms
from .models import Instrumento, InstrumentoEmprestimo
from alunos.models import Aluno

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ["nome", "descricao", "pertence_associacao", "ativo"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "identificador": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "pertence_associacao": forms.Select(attrs={"class": "form-select"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class InstrumentoEmprestimoForm(forms.ModelForm):
    class Meta:
        model = InstrumentoEmprestimo
        fields = ["aluno", "data_emprestimo", "data_devolucao", "observacao"]

        widgets = {
            "aluno": forms.Select(attrs={"class": "form-select"}),
            "data_emprestimo": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "data_devolucao": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "observacao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
