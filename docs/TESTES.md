# Guia de Testes e Cobertura de Código — ABANFAR BF

Documento completo com todos os comandos e configurações para executar testes e gerar relatórios de cobertura de código no projeto Django ABANFAR BF.

---

## 1. Ativação do Ambiente Virtual (venv)

Antes de executar qualquer comando, ative o ambiente virtual. Todos os comandos abaixo devem ser executados a partir da pasta interna `abanfar_bf/` (onde fica o `manage.py`).

**PowerShell (Windows):**
```powershell
# Da pasta raiz do projeto (abanfar-bf/)
..\venv\Scripts\Activate.ps1
```

**Prompt de Comando (CMD):**
```cmd
..\venv\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source ../venv/bin/activate
```

---

## 2. Instalação das Dependências

Se necessário, instale ou atualize as dependências listadas no `requirements.txt`:

```bash
pip install -r ../requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host pypi.python.org
```

---

## 3. Estrutura dos Arquivos de Teste

Os testes estão organizados por aplicativo Django. Cada app possui seu próprio arquivo (ou pasta) de testes:

| Aplicativo       | Arquivo(s) de Teste                         | Descrição                                    |
|------------------|---------------------------------------------|----------------------------------------------|
| `alunos`         | `alunos/test/test_views.py`                 | Views, CRUD, API de alunos                   |
| `blog`           | `blog/tests.py`                             | Views públicas do blog                       |
| `contas`         | `contas/tests.py`                           | Login, painéis, exportações, decorators      |
| `grupos`         | `grupos/tests.py`                           | CRUD de grupos, exportações, integrantes     |
| `instrumentos`   | `instrumentos/tests.py`                     | Inventário, IoT, empréstimos, exportações    |
| `materias`       | `materias/tests.py`                         | CRUD de matérias, matrículas                 |
| `professores`    | `professores/tests.py`                      | Ensaios, apresentações, CRUD, exportações    |
| `transparencia`  | `transparencia/tests.py`                    | Portal de transparência, publicações         |

> **Total:** 104 testes unitários cobrindo toda a aplicação.

---

## 4. Execução dos Testes

Execute os comandos sempre a partir do diretório `abanfar_bf/` (onde está o `manage.py`).

### 4.1 — Executor Padrão do Django

```bash
# Roda todos os 104 testes
python manage.py test

# Modo detalhado (verbose): mostra o nome de cada teste individualmente
python manage.py test --verbosity=2

# Rodar apenas um aplicativo específico
python manage.py test contas
python manage.py test alunos
python manage.py test grupos
python manage.py test instrumentos
python manage.py test professores
python manage.py test materias
python manage.py test transparencia
python manage.py test blog

# Rodar um TestCase específico
python manage.py test contas.tests.ContasTestCase

# Rodar um teste unitário específico
python manage.py test contas.tests.ContasTestCase.test_login_view_success_aluno
```

### 4.2 — Usando o Pytest (Recomendado)

O `pytest-django` já está configurado via `pytest.ini`. Oferece saída mais rica e filtros flexíveis:

```bash
# Roda todos os testes
pytest

# Modo detalhado com logs no terminal
pytest -v -s

# Roda apenas um aplicativo específico
pytest contas/
pytest alunos/
pytest grupos/
pytest instrumentos/

# Roda um arquivo de teste específico
pytest contas/tests.py

# Roda um teste pelo nome (substring match)
pytest -k "test_login"
pytest -k "test_exportar"

# Para ao primeiro erro (fail fast)
pytest -x

# Para ao primeiro erro com detalhes máximos
pytest -x -v --tb=long
```

---

## 5. Cobertura de Código (Coverage)

O `coverage` mede quais linhas do código foram executadas durante os testes.

### 5.1 — Coletar dados de cobertura

**Via Django test runner:**
```bash
coverage run --source='.' manage.py test
```

**Via Pytest (Recomendado):**
```bash
coverage run -m pytest
```

### 5.2 — Visualizar relatório no terminal

```bash
# Resumo simples
coverage report

# Com indicação de quais linhas NÃO foram cobertas
coverage report -m
```

### 5.3 — Gerar relatório HTML interativo

```bash
coverage html
```

Isso cria a pasta `htmlcov/`. Abra `htmlcov/index.html` no navegador para ver o relatório visual completo.

### 5.4 — Limpar dados de cobertura antigos

```bash
coverage erase
```

---

## 6. Comandos Rápidos (Atalhos Úteis)

```bash
# Rodar testes + cobertura + relatório HTML de uma vez
coverage run -m pytest && coverage html && echo "Relatório em htmlcov/index.html"

# Rodar apenas testes de exportação (Excel e PDF)
pytest -k "exportar" -v

# Verificar se todos os 104 testes passam antes de fazer commit
python manage.py test --verbosity=0
```

---

## 7. Funcionalidades Testadas por Exportação

Os testes de exportação cobrem os formatos **CSV**, **Excel (.xlsx)** e **PDF** para todos os módulos:

| Módulo        | CSV | Excel | PDF |
|---------------|-----|-------|-----|
| Alunos        | ✅  | ✅    | ✅  |
| Professores   | ✅  | ✅    | ✅  |
| Instrumentos  | ✅  | ✅    | ✅  |
| Grupos        | ✅  | ✅    | ✅  |
