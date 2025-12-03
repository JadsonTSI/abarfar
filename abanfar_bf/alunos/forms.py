from django import forms
from django.contrib.auth.models import User
from contas.models import Perfil
from .models import Aluno

class AlunoCadastroForm(forms.Form):
    nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    usuario = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        username = self.cleaned_data["usuario"]
        email = self.cleaned_data["email"]

        # Verifica duplicação de username
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Usuário já existe. Escolha outro nome de usuário.")

        # Verifica duplicação de email
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("E-mail já está em uso. Use outro e-mail.")

        # Criar o User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=self.cleaned_data["senha"],
            first_name=self.cleaned_data["nome"],
            last_name=self.cleaned_data["sobrenome"],
        )

        # Criar o Perfil (tipo aluno)
        perfil = Perfil.objects.create(
            user=user,
            tipo="aluno"
        )

        # Criar matrícula automática
        matricula = f"ALU{user.id:04d}"

        # Criar o Aluno
        aluno = Aluno.objects.create(
            perfil=perfil,
            nome=self.cleaned_data["nome"],
            sobrenome=self.cleaned_data["sobrenome"],
            telefone=self.cleaned_data["telefone"],
            matricula=matricula
        )

        return aluno
