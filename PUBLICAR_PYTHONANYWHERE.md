# Publicar o site de graça no PythonAnywhere

Passo a passo para colocar o sistema da ABANFAR BF no ar no plano **gratuito** do
PythonAnywhere, com **dados fictícios de demonstração** (nenhum dado real de aluno sai do seu computador).

- Endereço final: `https://SEUUSUARIO.pythonanywhere.com`
- Custo: R$ 0
- Tempo: uns 20 minutos

> Em todos os comandos abaixo, troque **`SEUUSUARIO`** pelo nome de usuário que você criar no PythonAnywhere.

---

## 1. Criar a conta

1. Acesse **pythonanywhere.com** → *Pricing & signup* → **Create a Beginner account** (gratuita).
2. O nome de usuário vira o endereço do site. Sugestão: `abanfarbf` → `abanfarbf.pythonanywhere.com`.
3. Confirme o e-mail.

## 2. Baixar o código

No painel do PythonAnywhere, abra **Consoles → Bash** e rode:

```bash
git clone --depth 1 https://github.com/JadsonTSI/abarfar.git
```

## 3. Criar o ambiente Python e instalar as dependências

```bash
mkvirtualenv --python=python3.11 abanfar
```

```bash
pip install -r ~/abarfar/requirements.txt
```

(A instalação leva alguns minutos. Se fechar o console, reative depois com `workon abanfar`.)

## 4. Criar o arquivo de configuração (`.env`)

Os comandos abaixo criam o `.env` já com uma chave secreta nova, sem você precisar copiá-la:

```bash
cd ~/abarfar/abanfar_bf
```

```bash
python -c "import secrets; print('DJANGO_SECRET_KEY=' + secrets.token_urlsafe(50))" > .env
```

```bash
echo "DJANGO_DEBUG=0" >> .env
```

```bash
echo "DJANGO_ALLOWED_HOSTS=SEUUSUARIO.pythonanywhere.com" >> .env
```

## 5. Preparar o banco e os dados de demonstração

```bash
python manage.py migrate
```

```bash
python manage.py collectstatic --noinput
```

```bash
python manage.py criar_dados_demo
```

O último comando mostra os logins **gerente.demo**, **professor.demo** e **aluno.demo** e uma
**senha**. **Anote a senha**: ela não fica salva em lugar nenhum. (Para gerar outra, rode o comando de novo.)

Opcional, para acessar o admin do Django (`/admin/`, onde ficam a Ouvidoria, mensagens de contato etc.):

```bash
python manage.py createsuperuser
```

## 6. Criar o site (aba **Web**)

1. **Web → Add a new web app → Next → Manual configuration** (não escolha "Django") **→ Python 3.11 → Next**.
2. Na página do site, preencha:
   - **Source code:** `/home/SEUUSUARIO/abarfar/abanfar_bf`
   - **Working directory:** `/home/SEUUSUARIO/abarfar/abanfar_bf`
   - **Virtualenv:** `/home/SEUUSUARIO/.virtualenvs/abanfar`
3. Em **WSGI configuration file**, clique no link do arquivo, **apague todo o conteúdo** e cole:

   ```python
   import os
   import sys

   path = '/home/SEUUSUARIO/abarfar/abanfar_bf'
   if path not in sys.path:
       sys.path.insert(0, path)

   os.environ['DJANGO_SETTINGS_MODULE'] = 'abanfar_bf.settings'

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

   Clique em **Save**.
4. Em **Static files**, adicione duas linhas:

   | URL | Directory |
   |---|---|
   | `/static/` | `/home/SEUUSUARIO/abarfar/abanfar_bf/staticfiles` |
   | `/media/` | `/home/SEUUSUARIO/abarfar/abanfar_bf/media` |

5. Em **Security**, ligue **Force HTTPS**.
6. Clique no botão verde **Reload** no topo da página.

Pronto: abra `https://SEUUSUARIO.pythonanywhere.com`.

---

## Atualizar o site depois de mudanças no código

No console Bash:

```bash
workon abanfar && cd ~/abarfar && git pull
```

```bash
cd abanfar_bf && python manage.py migrate && python manage.py collectstatic --noinput
```

Depois clique em **Reload** na aba **Web**.

## Manter o site no ar

No plano gratuito, o site é desligado se ninguém renovar. **Uma vez por mês**, entre na aba **Web** e
clique em **Run until 1 month from today**. O PythonAnywhere manda um e-mail uma semana antes do prazo.

## Limitações do plano gratuito

- Endereço `.pythonanywhere.com` (domínio próprio só no plano pago).
- 512 MB de espaço em disco, suficiente para este projeto.
- O e-mail de recuperação de senha pode não funcionar (o plano gratuito restringe conexões externas).
  Se precisar trocar uma senha, use o admin ou `python manage.py changepassword USUARIO`.
- A parte de IoT (ESP32/MQTT) não roda no plano gratuito.

## Se algo der errado

- Na aba **Web**, abra o **Error log** (o erro mais recente fica no fim do arquivo).
- `DisallowedHost`: o endereço em `DJANGO_ALLOWED_HOSTS` no `.env` está diferente do endereço do site.
- `Defina DJANGO_SECRET_KEY`: o `.env` não está em `~/abarfar/abanfar_bf/` ou está vazio (veja com `cat .env`).
- Site sem cores/estilos: confira o mapeamento `/static/` do passo 6 e rode o `collectstatic` de novo.
- Depois de qualquer mudança no `.env` ou no código, clique em **Reload**.
