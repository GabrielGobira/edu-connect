# 🎓 EduConnect

> API de gerenciamento escolar para controle de **alunos, notas, frequências e ocorrências**, desenvolvida com Python, FastAPI, SQLAlchemy e SQLite.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-API%20REST-009688?logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/Banco-SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

---

## Sumário

- [Sobre o projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Como executar](#como-executar)
- [Documentação da API](#documentação-da-api)
- [Banco de dados](#banco-de-dados)
- [Testes](#testes)
- [Como contribuir](#como-contribuir)
- [Licença](#licença)
- [Autor](#autor)

---

## Sobre o projeto

O **EduConnect** é uma API REST para gerenciamento escolar. Ela centraliza as informações acadêmicas e disciplinares da instituição, permitindo cadastrar e consultar alunos, notas, frequências e ocorrências em um só lugar, com validação dos dados e documentação interativa.

---

## Funcionalidades

- Cadastro, consulta e atualização de **alunos**.
- Cadastro e consulta de **notas**.
- Registro e consulta de **frequências**.
- Registro e consulta de **ocorrências**.

---

## Tecnologias utilizadas

- **Python**: linguagem principal do projeto.
- **FastAPI**: desenvolvimento da API REST.
- **SQLAlchemy**: mapeamento e manipulação do banco de dados.
- **SQLite**: banco de dados utilizado no projeto.
- **Pydantic**: validação dos dados recebidos pela API.
- **Pytest**: execução dos testes automatizados.
- **Git e GitHub**: versionamento e colaboração em equipe.

---

## Estrutura do projeto

```text
edu-connect/
├── app/
│   ├── models/       # Modelos do banco de dados
│   ├── schemas/      # Validação dos dados
│   ├── database.py   # Configuração do banco
│   ├── init_db.py    # Inicialização das tabelas
│   └── main.py       # Aplicação FastAPI
├── docs/
│   ├── BANCO_DE_DADOS.md
│   └── DER_EDUCONNECT.md
├── tests/            # Testes automatizados
├── requirements.txt  # Dependências
└── README.md         # Documentação principal
```

---

## Como executar

**1. Clone o repositório**

```bash
git clone https://github.com/GabrielGobira/edu-connect.git
cd edu-connect
```

**2. (Opcional) Crie e ative um ambiente virtual**

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

**4. Inicialize o banco de dados**

```bash
python -m app.init_db
```

**5. Execute a API**

```bash
uvicorn app.main:app --reload
```

A API ficará disponível em `http://127.0.0.1:8000`.

---

## Documentação da API

Com a API em execução, acesse a documentação interativa (Swagger UI):

👉 http://127.0.0.1:8000/docs

---

## Banco de dados

O EduConnect utiliza **SQLite** com **SQLAlchemy** para armazenar e gerenciar as informações escolares.

O banco possui cinco entidades principais:

- Usuários
- Alunos
- Notas
- Frequências
- Ocorrências

### Documentação do banco

- [Documentação do Banco de Dados](docs/BANCO_DE_DADOS.md)
- [Diagrama Entidade-Relacionamento (DER)](docs/DER_EDUCONNECT.md)

O DER apresenta as entidades, seus atributos, chaves primárias, chaves estrangeiras e relacionamentos.

---

## Testes

Para rodar os testes automatizados:

```bash
python -m pytest -v
```

---

## Como contribuir

1. Faça um **fork** do projeto.
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Faça commit das mudanças: `git commit -m "feat: adiciona minha feature"`
4. Envie para o seu fork: `git push origin feature/minha-feature`
5. Abra um **Pull Request**.

---

## Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

## Autor

**Gabriel Gobira**

- GitHub: [@GabrielGobira](https://github.com/GabrielGobira)
