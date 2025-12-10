from django import forms
from django.contrib.auth.models import User
from contas.models import Perfil
from .models import Aluno, GrupoMusical, Naipe
from instrumentos.models import Instrumento


class AlunoCadastroForm(forms.Form):
    nome = forms.CharField(max_length=100)
    sobrenome = forms.CharField(max_length=100)
    usuario = forms.CharField(max_length=100)
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    senha = forms.CharField(widget=forms.PasswordInput)

    instrumento = forms.ModelChoiceField(
        queryset=Instrumento.objects.all(),
        required=False
    )

    NAIPE_CHOICES = [
        ("Cordas", "Cordas"),
        ("Madeiras", "Madeiras"),
        ("Metais", "Metais"),
        ("Percussão", "Percussão"),
        ("Harmônicos", "Harmônicos"),
        ("Vocal", "Vocal"),
    ]

    naipe = forms.ChoiceField(choices=NAIPE_CHOICES, required=False)

    grupo = forms.ModelChoiceField(
        queryset=GrupoMusical.objects.none(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["grupo"].queryset = GrupoMusical.objects.all()

    def save(self):
        username = self.cleaned_data["usuario"]
        email = self.cleaned_data["email"]

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Usuário já existe.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("E-mail já está em uso.")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=self.cleaned_data["senha"],
            first_name=self.cleaned_data["nome"],
            last_name=self.cleaned_data["sobrenome"],
        )

        perfil = Perfil.objects.create(user=user, tipo="aluno")
        matricula = f"ALU{user.id:04d}"

        grupo = self.cleaned_data["grupo"]

        if grupo.nome.lower() == "musicalização":
            instrumento, _ = Instrumento.objects.get_or_create(nome="Flauta Doce")
            naipe = None
        else:
            instrumento = self.cleaned_data["instrumento"]
            naipe_nome = self.cleaned_data["naipe"]
            naipe, _ = Naipe.objects.get_or_create(nome=naipe_nome) if naipe_nome else (None, False)

        aluno = Aluno.objects.create(
            perfil=perfil,
            nome=self.cleaned_data["nome"],
            sobrenome=self.cleaned_data["sobrenome"],
            telefone=self.cleaned_data["telefone"],
            matricula=matricula,
            grupo=grupo,
            instrumento=instrumento,
            naipe=naipe,
        )

        return aluno


# --------------------------
#   FORMULÁRIO DE EDIÇÃO
# --------------------------
class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ["nome", "sobrenome", "telefone", "grupo", "instrumento", "naipe"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-control"}),
            "sobrenome": forms.TextInput(attrs={"class": "form-control"}),
            "telefone": forms.TextInput(attrs={"class": "form-control"}),

            "grupo": forms.Select(attrs={"class": "form-select"}),
            "instrumento": forms.Select(attrs={"class": "form-select"}),
            "naipe": forms.Select(attrs={"class": "form-select"}),
        }
