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

### Validação dos tipos de usuários (CHECK)

A tabela `usuarios` utiliza a restrição `ck_usuario_tipo`, permitindo somente os seguintes tipos:

- `admin`: administrador do sistema.
- `professor`: professor.

A restrição impede o cadastro de usuários com tipos inválidos diretamente no banco de dados.

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

Os testes incluem verificações de:

- Campos obrigatórios.
- Unicidade de registros.
- Integridade referencial.
- Intervalo permitido para notas.
- Duplicidade de registros de frequência.
- Exclusão de alunos com registros associados.
- Restrição dos tipos de usuários.
- Regras de negócio da aplicação.

### Resultado dos testes

Na execução validada em 27/11/2026:

| Indicador | Resultado |
|---|---|
| Testes aprovados | 84 |
| Testes reprovados | 0 |

A execução anterior apresentou um aviso de compatibilidade relacionado ao Starlette/httpx, sem impedir a aprovação dos testes.

## 7. Migração da tabela de usuários

Em 27/11/2026, foi realizada uma migração manual no banco de dados local para adicionar a restrição `ck_usuario_tipo`.

O procedimento envolveu:

- Criação de uma tabela temporária com a nova restrição.
- Transferência dos registros existentes.
- Substituição da tabela anterior.
- Recriação dos índices.
- Preservação do usuário administrador.
- Validação da nova restrição.

A tentativa de cadastrar um usuário com tipo inválido foi rejeitada pelo SQLite, retornando:

```text
CHECK constraint failed: ck_usuario_tipo
```

Esse resultado confirma o funcionamento da restrição.

A migração foi realizada no banco local. Outros bancos existentes precisam passar por uma migração equivalente.

## 8. Verificação da integridade do banco

Foram realizadas verificações diretamente no SQLite utilizando o DB Browser for SQLite.

### Integridade estrutural

```sql
PRAGMA integrity_check;
```

Resultado:

```text
ok
```

Nenhum problema de integridade estrutural foi identificado.

### Integridade referencial

```sql
PRAGMA foreign_key_check;
```

Resultado: nenhuma linha retornada.

Nenhuma violação de chave estrangeira foi identificada.

## 9. Dados de demonstração

O banco local foi populado com dados fictícios para facilitar os testes, a apresentação acadêmica e a demonstração das funcionalidades do sistema.

Os dados incluem alunos, notas, frequências e ocorrências escolares.

### Indicadores de frequência

| Indicador | Resultado |
|---|---|
| Total de registros | 201 |
| Presenças | 144 |
| Faltas | 57 |
| Percentual de presença | 71,64% |

### Ocorrências escolares

Foram identificados 12 registros de ocorrências escolares no banco local.

Os valores representam os dados de demonstração consultados em 27/11/2026 e podem mudar conforme novos registros forem cadastrados.

## 10. Relatórios SQL

O projeto possui consultas SQL para auxiliar na análise das informações escolares.

- Relatório geral de alunos.
- Relatório de notas.
- Relatório de frequência.
- Relatório de ocorrências.

As consultas utilizam recursos como:

- SELECT
- JOIN
- LEFT JOIN
- GROUP BY
- ORDER BY
- COUNT
- SUM
- AVG
- CASE

## 11. Arquivos principais

- `app/database.py`: configuração da conexão com o SQLite.
- `app/init_db.py`: inicialização das tabelas.
- `app/models/`: definição dos modelos SQLAlchemy.
- `tests/test_database.py`: testes automatizados do banco.
- `docs/DER_EDUCONNECT.md`: diagrama entidade-relacionamento.
- `docs/relatorio_geral_alunos.sql`: relatório geral.
- `docs/relatorio_notas.sql`: relatório de notas.
- `docs/relatorio_frequencia.sql`: relatório de frequência.
- `docs/relatorio_ocorrencias.sql`: relatório de ocorrências.
- `educonnect.db`: arquivo local do banco SQLite.

## 12. Tecnologias utilizadas

- Python
- SQLite
- SQLAlchemy
- pytest
- FastAPI
- DB Browser for SQLite
- Git e GitHub

## 13. Considerações finais

O banco de dados do EduConnect utiliza restrições de integridade para garantir a consistência das informações escolares.

A estrutura foi validada por 84 testes automatizados aprovados e verificações manuais realizadas diretamente no SQLite.

As melhorias realizadas reforçam a qualidade, a confiabilidade e a integridade dos dados armazenados.

A documentação deve ser mantida atualizada conforme novas funcionalidades e melhorias forem implementadas.

Última atualização: 27/11/2026.