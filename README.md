# EduConnect

API de gerenciamento escolar desenvolvida com Python, FastAPI, SQLAlchemy e SQLite.

## Tecnologias utilizadas

- Python — linguagem principal do projeto.
- FastAPI — desenvolvimento da API REST.
- SQLAlchemy — mapeamento e manipulação do banco de dados.
- SQLite — banco de dados utilizado no projeto.
- Pydantic — validação dos dados recebidos pela API.
- Pytest — execução dos testes automatizados.
- Git e GitHub — versionamento e colaboração em equipe.

## Banco de dados

O EduConnect utiliza SQLite com SQLAlchemy para armazenar
e gerenciar as informações escolares.

O banco de dados possui cinco entidades principais:

- Usuários
- Alunos
- Notas
- Frequências
- Ocorrências

### Documentação do banco

- [Documentação do Banco de Dados](docs/BANCO_DE_DADOS.md)
- [Diagrama Entidade-Relacionamento (DER)](docs/DER_EDUCONNECT.md)

O DER apresenta as entidades, seus atributos,
chaves primárias, chaves estrangeiras e relacionamentos.

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

## Funcionalidades
- Cadastro, consulta e atualização de alunos.
- Cadastro e consulta de notas.
- Registro e consulta de frequências.
- Registro e consulta de ocorrências.

## Como executar
1. Instale as dependências: pip install -r requirements.txt
2. Inicialize o banco: python -m app.init_db
3. Execute a API: uvicorn app.main:app --reload

## Documentação
Acesse http://127.0.0.1:8000/docs com a API em execução.

## Testes
Execute python -m pytest -v para rodar os testes automatizados.
