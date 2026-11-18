"""Cria dados fictícios para demonstração do sistema (nenhum dado real).

Uso:
    python manage.py criar_dados_demo                 # gera uma senha aleatória e mostra no final
    python manage.py criar_dados_demo --senha XYZ     # usa a senha informada para os 3 usuários

Pode ser executado mais de uma vez: o que já existe é reaproveitado.
"""
import datetime
import secrets

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from alunos.models import Aluno, GrupoMusical, Naipe
from contas.models import Perfil
from instrumentos.models import Instrumento, InstrumentoEmprestimo
from materias.models import Materia, MatriculaMateria
from professores.models import ApresentacaoModel, EnsaiosproModel, ProfessorModel

DIAS = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]

NAIPES = {
    "Madeiras": ["Flauta transversal", "Clarinete", "Saxofone alto"],
    "Metais": ["Trompete", "Trombone", "Tuba"],
    "Percussão": ["Caixa clara", "Bumbo", "Pratos"],
    "Cordas": ["Violino", "Violão", "Contrabaixo"],
}

ALUNOS_FICTICIOS = [
    ("Ana", "Lima", "Madeiras", "Flauta transversal", "Banda Musical"),
    ("Bruno", "Costa", "Metais", "Trompete", "Banda Musical"),
    ("Carla", "Mendes", "Percussão", "Caixa clara", "Banda Musical"),
    ("Diego", "Rocha", "Cordas", "Violino", "Orquestra"),
    ("Elisa", "Nunes", "Madeiras", "Clarinete", "Orquestra"),
    ("Felipe", "Araújo", "Metais", "Trombone", "Banda Musical"),
    ("Gabriela", "Pires", "Cordas", "Violão", "Orquestra de Flautas"),
]


class Command(BaseCommand):
    help = "Cria usuários e dados FICTÍCIOS para demonstração (gerente, professor e aluno)."

    def add_arguments(self, parser):
        parser.add_argument("--senha", help="Senha dos usuários de demonstração (padrão: gerada aleatoriamente).")

    @transaction.atomic
    def handle(self, *args, **opts):
        senha = opts.get("senha") or secrets.token_urlsafe(9)
        hoje = timezone.localdate()

        # Grupos, naipes e instrumentos
        grupos = {nome: GrupoMusical.objects.get_or_create(nome=nome, defaults={"descricao": f"Grupo {nome} (demonstração)"})[0]
                  for nome in ("Banda Musical", "Orquestra", "Orquestra de Flautas")}
        naipes, instrumentos = {}, {}
        condicoes = ["otimo", "otimo", "bom", "bom", "regular", "ruim"]
        for i, (naipe_nome, nomes_inst) in enumerate(NAIPES.items()):
            naipe, _ = Naipe.objects.get_or_create(nome=naipe_nome)
            naipes[naipe_nome] = naipe
            for j, nome_inst in enumerate(nomes_inst):
                inst = Instrumento.objects.filter(nome=nome_inst).first()
                if inst is None:
                    inst = Instrumento.objects.create(
                        nome=nome_inst, descricao="Instrumento de demonstração",
                        condicao=condicoes[(i + j) % len(condicoes)],
                    )
                naipe.instrumentos.add(inst)
                instrumentos[nome_inst] = inst

        # Usuários de demonstração
        def usuario(username, tipo, nome, sobrenome):
            user, _ = User.objects.get_or_create(username=username, defaults={"first_name": nome, "last_name": sobrenome})
            user.first_name, user.last_name = nome, sobrenome
            user.set_password(senha)
            user.save()
            perfil, _ = Perfil.objects.get_or_create(user=user, defaults={"tipo": tipo})
            if perfil.tipo != tipo:
                perfil.tipo = tipo
                perfil.save()
            return perfil

        usuario("gerente.demo", "gerente", "Gestora", "Demonstração")
        perfil_prof = usuario("professor.demo", "professor", "Paulo", "Demonstração")
        professor, _ = ProfessorModel.objects.get_or_create(perfil=perfil_prof, defaults={
            "nome": "Paulo Demonstração", "email": "professor.demo@example.com",
            "telefone": "(84) 90000-0000", "instrumento": "Trompete",
        })

        # Alunos (o primeiro é o login aluno.demo; os outros só existem como cadastro)
        alunos = []
        for n, (nome, sobrenome, naipe_nome, inst_nome, grupo_nome) in enumerate(ALUNOS_FICTICIOS, start=1):
            username = "aluno.demo" if n == 1 else f"aluno.demo{n}"
            perfil = usuario(username, "aluno", nome, sobrenome)
            if n > 1:
                perfil.user.set_unusable_password()  # só o aluno.demo entra no sistema
                perfil.user.save()
            aluno, _ = Aluno.objects.get_or_create(perfil=perfil, defaults={
                "nome": nome, "sobrenome": sobrenome, "matricula": f"DEMO{n:03d}",
                "instrumento": instrumentos[inst_nome], "naipe": naipes[naipe_nome], "grupo": grupos[grupo_nome],
            })
            alunos.append(aluno)

        # Matérias e matrículas
        for nome_materia in ("Teoria Musical I", "Prática de Conjunto", "Percepção Rítmica"):
            materia, _ = Materia.objects.get_or_create(nome=nome_materia, defaults={"professor": professor})
            for aluno in alunos[:5]:
                MatriculaMateria.objects.get_or_create(materia=materia, aluno=aluno)

        # Ensaios e apresentações futuras
        for d, (nome, local) in enumerate([("Ensaio geral da banda", "Sede da ABANFAR BF"),
                                            ("Ensaio de naipe — Metais", "Sala 2"),
                                            ("Ensaio da orquestra", "Auditório municipal")]):
            data = hoje + datetime.timedelta(days=3 + d * 4)
            EnsaiosproModel.objects.get_or_create(nome=nome, data=data, defaults={
                "dia_semana": DIAS[data.weekday()], "inicio": datetime.time(18, 30),
                "fim": datetime.time(20, 30), "local": local,
            })
        for d, (titulo, local) in enumerate([("Retreta na Praça Central", "Praça Central de Baía Formosa"),
                                              ("Concerto de fim de ano", "Igreja Matriz")]):
            ApresentacaoModel.objects.get_or_create(titulo=titulo, defaults={
                "descricao": "Apresentação de demonstração", "data": hoje + datetime.timedelta(days=10 + d * 20),
                "horario": "19:00", "horario_fim": "21:00", "local": local, "grupo": "Banda Musical",
            })

        # Alguns empréstimos (um deles atrasado, para aparecer nos alertas do gerente)
        for aluno, dias_atras in ((alunos[1], 3), (alunos[3], 25)):
            InstrumentoEmprestimo.objects.get_or_create(
                instrumento=aluno.instrumento, aluno=aluno, devolvido=False,
                defaults={"data_emprestimo": hoje - datetime.timedelta(days=dias_atras)},
            )

        self.stdout.write(self.style.SUCCESS("Dados de demonstração prontos (todos fictícios)."))
        self.stdout.write("Logins (mesma senha para os três):")
        for login in ("gerente.demo", "professor.demo", "aluno.demo"):
            self.stdout.write(f"  - {login}")
        self.stdout.write(f"Senha: {senha}")
        self.stdout.write(self.style.WARNING("Guarde a senha agora; ela não fica salva em lugar nenhum."))
