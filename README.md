# AdotePet
Github para o projeto de Sistemas Distribuídos I
## Configuração do ambiente

### Pré-requisitos

Antes de executar o projeto, certifique-se de possuir:

- Python 3.8
- pip
- Git

Para verificar a versão instalada do Python:

```bash
python --version
```

O projeto foi desenvolvido utilizando **Python 3.8** e **Django 3.1.7**.

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd AdotePet
```

### 2. Criar o ambiente virtual

No Windows, caso existam múltiplas versões do Python instaladas, utilize:

```bash
py -3.8 -m venv venv
```

Ative o ambiente virtual:

```bash
.\venv\Scripts\activate
```

Após a ativação, `(venv)` deverá aparecer no terminal.

### 3. Instalar as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install -r requirements.txt
```

### 4. Aplicar as migrações

Para criar/atualizar as tabelas do banco de dados de acordo com as migrações existentes:

```bash
python manage.py migrate
```

É possível verificar o estado das migrações com:

```bash
python manage.py showmigrations
```

As migrações marcadas com `[X]` já foram aplicadas ao banco de dados.

### 5. Executar o servidor

```bash
python manage.py runserver
```

Por padrão, a aplicação ficará disponível em:

```text
http://127.0.0.1:8000/
```

O painel administrativo do Django pode ser acessado em:

```text
http://127.0.0.1:8000/admin/
```

---

## Estrutura do projeto

A estrutura principal do projeto é organizada da seguinte maneira:

```text
AdotePet/
│
├── adocao/
│   ├── migrations/       # Migrações do banco de dados
│   ├── admin.py          # Configuração do Django Admin
│   ├── apps.py           # Configuração do aplicativo
│   ├── models.py         # Modelos e relacionamentos do sistema
│   ├── tests.py          # Testes da aplicação
│   └── views.py          # Views da aplicação
│
├── projetoSD/
│   ├── settings.py       # Configurações gerais do projeto
│   ├── urls.py           # Rotas principais
│   ├── asgi.py           # Configuração ASGI
│   └── wsgi.py           # Configuração WSGI
│
├── db.sqlite3            # Banco de dados SQLite
├── manage.py             # Utilitário de gerenciamento do Django
├── requirements.txt      # Dependências Python
└── README.md             # Documentação do projeto
```

### Aplicação `adocao`

A aplicação `adocao` concentra as funcionalidades relacionadas ao processo de adoção.

Os principais arquivos são:

- **`models.py`** — definição das entidades e seus relacionamentos no banco de dados.
- **`admin.py`** — configuração da visualização e gerenciamento dos dados pelo Django Admin.
- **`migrations/`** — histórico das alterações realizadas na estrutura do banco de dados.
- **`views.py`** — lógica responsável pelo processamento das requisições da aplicação.

### Projeto `projetoSD`

Contém as configurações gerais do Django.

- **`settings.py`** — aplicações instaladas, banco de dados e demais configurações.
- **`urls.py`** — define as principais rotas disponíveis.
- **`wsgi.py` e `asgi.py`** — pontos de entrada utilizados para execução/deploy da aplicação.
