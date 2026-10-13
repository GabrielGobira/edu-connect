# EduConnect

API de gerenciamento escolar desenvolvida com Python, FastAPI, SQLAlchemy e SQLite.

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
