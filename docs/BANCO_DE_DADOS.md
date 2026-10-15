
# Documentação do Banco de Dados — EduConnect

## 1. Visão geral

O EduConnect é um sistema de gerenciamento escolar desenvolvido em Python, utilizando SQLAlchemy como ORM e SQLite como banco de dados.

O banco armazena informações de usuários, alunos, notas, frequências e ocorrências escolares.

## 2. Estrutura do banco

O banco possui cinco tabelas principais:

| Tabela | Finalidade |
|---|---|
| usuarios | Armazenar dados dos usuários do sistema |
| alunos | Armazenar informações dos alunos |
| notas | Registrar notas dos alunos |
| frequencias | Controlar a presença dos alunos |
| ocorrencias | Registrar ocorrências escolares |

## 3. Relacionamentos

A tabela `alunos` possui relacionamentos de um para muitos (1:N) com:

- `notas`: um aluno pode possuir várias notas.
- `frequencias`: um aluno pode possuir vários registros de frequência.
- `ocorrencias`: um aluno pode possuir várias ocorrências.

As tabelas relacionadas utilizam o campo `aluno_id` como chave estrangeira, referenciando `alunos.id`.

## 4. Regras de integridade

### Chaves primárias (PRIMARY KEY)

Cada tabela possui um campo `id` que identifica seus registros.

### Chaves estrangeiras (FOREIGN KEY)

As tabelas `notas`, `frequencias` e `ocorrencias` possuem chaves estrangeiras para a tabela `alunos`.

O SQLite é configurado para habilitar a verificação de chaves estrangeiras por conexão.

### Campos obrigatórios (NOT NULL)

Os campos definidos como obrigatórios não aceitam valores nulos.

### Valores únicos (UNIQUE)

- A matrícula de cada aluno deve ser única.
- O e-mail de cada usuário deve ser único.
- Um aluno não pode possuir dois registros de frequência na mesma data.

### Validação de notas (CHECK)

A tabela `notas` utiliza a restrição `ck_nota_intervalo`, permitindo somente notas entre 0 e 10.

### Exclusão de alunos

O banco impede a exclusão de alunos que possuem notas, frequências ou ocorrências associadas, preservando a integridade referencial.

## 5. Inicialização do banco

Na raiz do projeto, execute:

```bash
python -m app.init_db
```

O comando cria as tabelas que ainda não existem, utilizando os modelos SQLAlchemy.

**Atenção:** `create_all()` não atualiza automaticamente a estrutura de tabelas já existentes. Alterações de esquema exigem um procedimento de migração apropriado.

## 6. Testes automatizados

O projeto utiliza pytest para validar o funcionamento da aplicação e do banco.

Execute todos os testes:

```bash
python -m pytest -v
```

Execute somente os testes de banco:

```bash
python -m pytest tests/test_database.py -v
```

Os testes incluem verificações de campos obrigatórios, unicidade, integridade referencial e regras de negócio.

Na última execução validada, a suíte completa apresentou 55 testes aprovados.

## 7. Arquivos principais

- `app/database.py`: configuração da conexão com o SQLite.
- `app/init_db.py`: inicialização das tabelas.
- `app/models/`: definição dos modelos SQLAlchemy.
- `tests/test_database.py`: testes automatizados do banco.
- `educonnect.db`: arquivo local do banco SQLite.

## 8. Tecnologias utilizadas

- Python
- SQLite
- SQLAlchemy
- pytest

## 9. Considerações finais

O banco de dados do EduConnect utiliza restrições de integridade para garantir a consistência das informações escolares.

A estrutura foi validada por testes automatizados, incluindo verificações de relacionamentos, campos obrigatórios e restrições do SQLite.
