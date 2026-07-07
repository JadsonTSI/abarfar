from django import forms
from django.contrib.auth.models import User
from .models import EnsaiosproModel, ApresentacaoModel, ProfessorModel
from contas.models import Perfil


# ENSAIOS
class EnsaiosForm(forms.ModelForm):
    class Meta:
        model = EnsaiosproModel
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Metais, Percussão...'}),
            'dia_semana': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'fim': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Sala de Ensaios, Auditório...'}),
        }


# APRESENTAÇÕES
class ApresentacaoForm(forms.ModelForm):
    class Meta:
        model = ApresentacaoModel
        fields = "__all__"
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Concerto de Primavera...'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Breve descrição...'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'horario': forms.TextInput(attrs={'class': 'form-control'}),
            'horario_fim': forms.TextInput(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Auditório Principal...'}),
            'grupo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Banda Sinfônica...'}),
        }


# CADASTRO PROFESSOR
class ProfessorForm(forms.Form):
    usuario = forms.CharField(max_length=150, label="Usuário")
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    instrumento = forms.CharField(max_length=100)
    ativo = forms.BooleanField(required=False)
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")

    def save(self):
        # salvar usuário de login
        user = User.objects.create_user(
            username=self.cleaned_data["usuario"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["senha"],
            first_name=self.cleaned_data["nome"]
        )

        # criar perfil
        perfil = Perfil.objects.create(
            user=user,
            tipo="professor"
        )

        # salvar tabela professor
        professor = ProfessorModel.objects.create(
            perfil=perfil,  # já liga o perfil ao professor 
            nome=self.cleaned_data["nome"],
            email=self.cleaned_data["email"],
            telefone=self.cleaned_data["telefone"],
            instrumento=self.cleaned_data["instrumento"],
            ativo=self.cleaned_data.get("ativo", True)
        )

        return professor


# FORMULÁRIO DE EDIÇÃO
class ProfessorEditForm(forms.ModelForm):
    class Meta:
        model = ProfessorModel
        fields = ["nome", "email", "telefone", "instrumento", "ativo"]

