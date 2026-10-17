# edu-connect
Sistema de gestão escolar para controle de alunos, notas, frequência e ocorrências .

API de gerenciamento escolar desenvolvida com Python, FastAPI, SQLAlchemy e SQLite.

![CI](https://github.com/GabrielGobira/edu-connect/actions/workflows/ci.yml/badge.svg)

## Funcionalidades

- Cadastro, consulta e atualização de alunos.
- Cadastro e consulta de notas.
- Registro e consulta de frequências.
- Registro e consulta de ocorrências.

## Tecnologias

- Python
- FastAPI
- SQLAlchemy + SQLite
- pytest
- GitHub Actions (integração contínua)

## Estrutura do projeto

```
edu-connect/
├── app/                 # código da API
├── docs/                # documentação técnica (banco de dados)
├── tests/               # testes automatizados
├── .github/workflows/   # pipeline de CI (ci.yml)
├── requirements.txt
└── README.md
```

## Como executar

1. Instale as dependências: `pip install -r requirements.txt`
2. Inicialize o banco: `python -m app.init_db`
3. Execute a API: `uvicorn app.main:app --reload`

## Documentação da API

Acesse <http://127.0.0.1:8000/docs> com a API em execução.

## Testes

Execute `python -m pytest -v` para rodar os testes automatizados.

## Fluxo de trabalho (GitFlow)

O projeto usa GitFlow simplificado:

| Branch | Função |
| --- | --- |
| `main` | Versão estável, pronta para entrega |
| `develop` | Integração das funcionalidades em andamento |
| `feature/<nome>` | Nova funcionalidade, criada a partir de `develop` |
| `fix/<nome>` | Correção de bug, criada a partir de `develop` |

Regras do grupo:

1. Nunca fazer commit direto em `main` ou `develop`.
2. Criar a branch a partir de `develop` e abrir Pull Request de volta para `develop`.
3. Pelo menos um integrante revisa o Pull Request antes do merge.
4. O merge só acontece com o CI verde.

## Commits semânticos

Os commits seguem o padrão Conventional Commits:

| Prefixo | Uso |
| --- | --- |
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `test:` | Criação ou ajuste de testes |
| `refactor:` | Refatoração sem mudar comportamento |
| `docs:` | Documentação |
| `ci:` | Pipeline de integração contínua |
| `chore:` | Tarefas gerais e configuração |

Exemplo: `feat: adiciona atualização de frequências e ocorrências`

## Integração contínua (CI)

O workflow `.github/workflows/ci.yml` roda automaticamente a cada push e a cada Pull Request em `main` e `develop`. Ele instala as dependências e executa `python -m pytest -v`. O resultado aparece na aba **Actions** do GitHub e no próprio Pull Request.

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE).
