# ABANFAR – BF  
## *O Silêncio Pede Música*

![Logo Abanfar](https://github.com/JadsonTSI/abarfar/blob/main/abanfar_bf/blog/static/img/logo_abanfar.png)

Sistema web desenvolvido em **Django** para gerenciamento da escola de música **ABANFAR – BF**, oferecendo ferramentas para organização de professores, ensaios, alunos e atividades internas.

---

## 🚀 Tecnologias Utilizadas
- Python 3.11+
- Django 5
- Bootstrap 5
- HTML & CSS
- SQLite3
- Git & GitHub

---

## 📌 Funcionalidades

### 🔐 Autenticação
- Login e logout
- Proteção de páginas
- Painel restrito

### 👨‍🏫 Professores
- Cadastro
- Edição
- Exclusão
- Listagem completa

### 🥁 Ensaios
- Registro de ensaios
- Relacionamento com professor

### 👥 Alunos *(em desenvolvimento)*
- Cadastro
- Listagem

### 📚 Cursos e Turmas *(em desenvolvimento)*

---
📁 Estrutura do Projeto
```
meu_projeto/
│
├── pasta1/
│   ├── arquivo1.py
│   └── arquivo2.py
│
├── pasta2/
│   ├── subpasta/
│   │   └── arquivo3.py
│   └── arquivo4.py
│
└── manage.py
```

yaml
Copiar código

---

## ⚙️ Como Rodar o Projeto

### 1️⃣ Clone o repositório
git clone https://github.com/JadsonTSI/abarfar.git
cd abarfar

shell
Copiar código

### 2️⃣ Crie e ative o ambiente virtual
python -m venv venv
venv/Scripts/activate # Windows
source venv/bin/activate # Linux/macOS

shell
Copiar código

### 3️⃣ Instale as dependências
pip install -r requirements.txt

shell
Copiar código

### 4️⃣ Rode as migrações
python manage.py migrate

shell
Copiar código

### 5️⃣ Crie um usuário administrador
python manage.py createsuperuser

shell
Copiar código

### 6️⃣ Inicie o servidor
python manage.py runserver

yaml
Copiar código

Acesse:  
**http://127.0.0.1:8000/**

---

## 🛠️ Roadmap

- Área do aluno  
- Controle de presença  
- Notas e desempenho  
- Dashboard administrativo  
- API REST  
- Exportação de relatórios PDF  

---

## 👤 Autor

**Jadson Leitão**  
Estudante de Sistemas para Internet • Desenvolvedor Django  

---
