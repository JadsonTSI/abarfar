<img src="https://github.com/JadsonTSI/abarfar/blob/main/abanfar_bf/blog/static/img/logo_abanfar.png" width="220"/>
🎵 ABANFAR – BF
O Silêncio Pede Música

Sistema web desenvolvido em Django para gerenciar atividades da escola de música ABANFAR – BF, incluindo controle de professores, alunos, ensaios, cursos e administração geral.
O objetivo é facilitar a organização e modernizar o ambiente escolar.

🚀 Tecnologias Utilizadas

Python 3.11+

Django 5

Bootstrap 5

HTML & CSS

SQLite3

Django Template Language

Git & GitHub

📌 Funcionalidades do Sistema
🔐 Autenticação

Login e logout

Controle de acesso

Perfis de usuário (Admin, Professores, etc.)

👨‍🏫 Professores

Cadastro

Edição

Exclusão

Listagem completa

🎼 Ensaios / Aulas

Registro de ensaios

Organização por data

Vinculação ao professor

👥 Alunos (futuro módulo)

Cadastro e gerenciamento

📚 Cursos / Turmas (futuro módulo)
📁 Estrutura do Projeto
abanfar_bf/
│
├── blog/
│   ├── static/
│   │   └── img/
│   │       └── logo_abanfar.png
│   ├── templates/
│   └── ...
│
├── professores/
│   ├── static/professores/
│   │   ├── professor.css
│   │   └── ensaios_pro.css
│   ├── templates/professores/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── projeto_abanfar/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
└── manage.py

⚙️ Como Rodar o Projeto Localmente
1️⃣ Clone o repositório
git clone https://github.com/JadsonTSI/abarfar.git
cd abarfar

2️⃣ Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/macOS

3️⃣ Instale as dependências
pip install -r requirements.txt

4️⃣ Aplique as migrações
python manage.py migrate

5️⃣ Crie um superusuário
python manage.py createsuperuser

6️⃣ Inicie o servidor
python manage.py runserver


Acesse em:
👉 http://127.0.0.1:8000/

🛠️ Roadmap – Próximos Recursos

Área exclusiva do aluno

Módulo financeiro

Controle de presença

Registro de notas e desempenho

Exportação de relatórios em PDF

API REST (Django Rest Framework)

Dashboard administrativo

👤 Autor

Jadson Leitão
Estudante de Sistemas para Internet • Desenvolvedor Backend (Django)
Projeto oficial da escola ABANFAR – BF
