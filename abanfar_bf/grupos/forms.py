from django import forms
from .models import Partitura
from alunos.models import GrupoMusical

class PartituraForm(forms.ModelForm):
    class Meta:
        model = Partitura
        fields = ["titulo", "arquivo"]

class GrupoForm(forms.ModelForm):
    class Meta:
        model = GrupoMusical
        fields = ["nome", "descricao"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }