# EduConnect — Sistema de Gestão Escolar

<p align="center">
  <img src="frontend/images/logo-educonnect.png" alt="Logomarca EduConnect" width="300">
</p>

<p align="center">
  <strong>Sistema de gestão escolar desenvolvido para centralizar e organizar informações acadêmicas.</strong>
</p>

<p align="center">
  Python • FastAPI • SQLite • SQLAlchemy • HTML • CSS • JavaScript
</p>

---

## 1. Sobre o projeto

O **EduConnect** é um sistema de gestão escolar desenvolvido como projeto acadêmico para a disciplina de Gestão e Qualidade de Software.

A aplicação tem como finalidade organizar e centralizar informações relacionadas à rotina escolar, oferecendo recursos para o gerenciamento de alunos, notas, frequências e ocorrências.

O projeto é composto por uma API REST, responsável pelas regras de negócio, validação e persistência dos dados, e por uma interface web que permite aos usuários interagir com as funcionalidades do sistema.

A proposta é contribuir para uma gestão escolar mais organizada, reduzir inconsistências nos registros e facilitar o acesso às informações acadêmicas.

## 2. Objetivos

### Objetivo geral

Desenvolver um sistema de gestão escolar que centralize informações acadêmicas por meio de uma API integrada a uma interface web, aplicando boas práticas de desenvolvimento e qualidade de software.

### Objetivos específicos

- Organizar os registros escolares em um banco de dados relacional.
- Disponibilizar operações de cadastro, consulta, atualização e exclusão conforme os recursos de cada módulo.
- Implementar validações para garantir maior consistência dos dados.
- Desenvolver uma interface web simples e intuitiva.
- Implementar autenticação para controlar o acesso ao sistema.
- Criar testes automatizados para verificar o funcionamento da aplicação.
- Utilizar Git e GitHub para versionamento e colaboração entre os integrantes.

## 3. Problema identificado e solução proposta

Na rotina escolar, informações de alunos, notas, frequências e ocorrências precisam ser registradas e consultadas constantemente.

Quando esses dados são mantidos em controles separados ou processos manuais, podem surgir problemas como:

- Informações duplicadas ou inconsistentes.
- Dificuldade para localizar registros.
- Erros durante o lançamento de informações.
- Retrabalho na atualização dos dados.
- Dificuldade no acompanhamento da situação acadêmica dos estudantes.

O EduConnect propõe uma solução centralizada, utilizando uma aplicação web integrada a uma API e a um banco de dados, permitindo organizar os principais registros escolares em um único ambiente.

## 4. Funcionalidades do sistema

A aplicação está organizada em quatro módulos principais.

### 4.1. Gerenciamento de alunos

Permite administrar os registros dos estudantes.

Principais recursos:

- Cadastro de alunos.
- Listagem dos alunos cadastrados.
- Consulta das informações dos estudantes.
- Edição dos dados cadastrais.
- Exclusão de registros, respeitando as regras de integridade do banco de dados.

### 4.2. Gerenciamento de notas

Permite registrar e consultar informações relacionadas ao desempenho acadêmico.

Principais recursos:

- Cadastro de notas.
- Consulta dos registros cadastrados.
- Visualização do histórico de notas.
- Exclusão de registros de notas.

### 4.3. Gerenciamento de frequência

Permite registrar e acompanhar a frequência dos estudantes.

Principais recursos:

- Registro de frequência.
- Consulta do histórico de frequência.
- Filtragem de registros por aluno.
- Atualização de registros por meio da API.
- Exclusão de registros.
- Validação para impedir registros duplicados para o mesmo aluno na mesma data.

### 4.4. Gerenciamento de ocorrências

Permite registrar e consultar ocorrências relacionadas aos estudantes.

Principais recursos:

- Cadastro de ocorrências.
- Consulta do histórico de ocorrências.
- Filtragem de registros por aluno.
- Atualização de registros por meio da API.
- Exclusão de ocorrências.

## 5. Tecnologias utilizadas

O EduConnect utiliza tecnologias voltadas ao desenvolvimento de aplicações web, construção de APIs, persistência de dados e testes automatizados.

| Tecnologia | Aplicação no projeto |
|---|---|
| Python | Linguagem principal do backend. |
| FastAPI | Construção da API REST e gerenciamento das rotas. |
| SQLAlchemy | Mapeamento objeto-relacional e acesso ao banco de dados. |
| SQLite | Armazenamento das informações da aplicação. |
| Pydantic | Validação e estruturação dos dados recebidos. |
| HTML5 | Estrutura da interface web. |
| CSS3 | Estilização e identidade visual do sistema. |
| JavaScript | Interatividade e comunicação com a API. |
| Pytest | Execução dos testes automatizados. |
| Git | Controle de versão do código-fonte. |
| GitHub | Hospedagem do repositório e colaboração em equipe. |
| Uvicorn | Servidor utilizado para executar a aplicação FastAPI. |

## 6. Arquitetura da aplicação

O sistema utiliza uma arquitetura dividida entre frontend, backend e banco de dados.

### Frontend

Responsável pela apresentação das informações e interação com o usuário.

Desenvolvido com HTML, CSS e JavaScript, disponibiliza telas para autenticação, cadastro e consulta dos registros escolares.

### Backend

Responsável pelo processamento das requisições, aplicação das regras de negócio, autenticação e validação dos dados.

Desenvolvido com Python e FastAPI.

### Banco de dados

Responsável pelo armazenamento persistente das informações da aplicação.

Utiliza SQLite, com acesso aos registros realizado por meio do SQLAlchemy.

### Fluxo de funcionamento

```text
       USUÁRIO
          |
          v
   INTERFACE WEB
  HTML / CSS / JS
          |
          v
      API REST
       FastAPI
          |
          v
   REGRAS E VALIDAÇÕES
       Pydantic
          |
          v
      SQLAlchemy
          |
          v
       SQLITE
   Banco de dados
```

A comunicação entre frontend e backend ocorre por meio de requisições HTTP. As operações são processadas pela API, que realiza as validações necessárias e acessa o banco de dados.

## 7. Banco de dados

O EduConnect utiliza o SQLite como sistema de gerenciamento de banco de dados, integrado ao SQLAlchemy.

A estrutura possui cinco entidades principais:

| Entidade | Responsabilidade |
|---|---|
| Usuários | Armazenar informações relacionadas aos usuários e à autenticação. |
| Alunos | Manter os dados cadastrais dos estudantes. |
| Notas | Armazenar os registros de desempenho acadêmico. |
| Frequências | Registrar a situação de frequência dos estudantes. |
| Ocorrências | Armazenar ocorrências associadas aos alunos. |

A estrutura utiliza chaves primárias e estrangeiras para identificar os registros e estabelecer relacionamentos entre as entidades.

### Documentação complementar

- [Documentação do Banco de Dados](docs/BANCO_DE_DADOS.md)
- [Diagrama Entidade-Relacionamento (DER)](docs/DER_EDUCONNECT.md)

O diagrama apresenta a organização das entidades, seus atributos, chaves e relacionamentos.

## 8. Autenticação e segurança

O sistema possui mecanismo de autenticação para controlar o acesso às funcionalidades protegidas.

A comunicação autenticada entre frontend e backend utiliza token no padrão Bearer.

O frontend armazena o token durante a sessão de utilização e o envia nas requisições que exigem autenticação.

O backend também utiliza regras de autorização para restringir determinadas operações a usuários administradores.

**Cuidados de segurança:**

- Não armazenar senhas ou chaves secretas diretamente no código-fonte.
- Utilizar variáveis de ambiente para configurar segredos da aplicação.
- Não compartilhar tokens de autenticação.
- Não versionar arquivos com credenciais ou informações sensíveis.
- Utilizar uma chave secreta adequada e protegida em ambientes de produção.

## 9. Estrutura do projeto

O repositório está organizado para separar as responsabilidades da aplicação.

```text
edu-connect/
│
├── app/
│   ├── models/
│   │   ├── usuario.py
│   │   ├── aluno.py
│   │   ├── nota.py
│   │   ├── frequencia.py
│   │   └── ocorrencia.py
│   │
│   ├── schemas/
│   │   └── Schemas de validação
│   │
│   ├── database.py
│   ├── init_db.py
│   └── main.py
│
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── images/
│   │   └── logo-educonnect.png
│   ├── js/
│   │   ├── api.js
│   │   └── app.js
│   └── index.html
│
├── docs/
│   ├── BANCO_DE_DADOS.md
│   └── DER_EDUCONNECT.md
│
├── scripts/
│   └── Scripts auxiliares
│
├── tests/
│   └── Testes automatizados
│
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

**Observação:** a estrutura apresenta os principais diretórios e arquivos do projeto. Alguns arquivos auxiliares foram agrupados para facilitar a leitura.

## 10. Instalação e configuração

Para executar o EduConnect localmente, é necessário ter instalado:

- Python 3.12 ou compatível com as dependências do projeto.
- Git.
- Visual Studio Code ou outro editor de código.
- Extensão Live Server no VS Code, para executar o frontend.

### 10.1. Clonar o repositório

```bash
git clone https://github.com/GabrielGobira/edu-connect.git
```

Acesse a pasta:

```bash
cd edu-connect
```

### 10.2. Criar ambiente virtual

```bash
py -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 10.3. Instalar as dependências

```bash
py -m pip install -r requirements.txt
```

### 10.4. Configurar a chave de autenticação

No PowerShell, configure a variável de ambiente utilizada pela aplicação:

```powershell
$env:EDUCONNECT_JWT_SECRET = "sua-chave-local-de-desenvolvimento"
```

Utilize uma chave apropriada para cada ambiente. Não compartilhe nem versione essa informação.

### 10.5. Inicializar o banco de dados

```bash
py -m app.init_db
```

Esse comando executa o processo de inicialização do banco de dados e das tabelas da aplicação.

### 10.6. Executar o backend

```bash
py -m uvicorn app.main:app --reload
```

Com a aplicação em execução, a API estará disponível em:

```text
http://127.0.0.1:8000
```

### 10.7. Executar o frontend

Com o backend em funcionamento:

1. Abra a pasta `frontend` no Visual Studio Code.
2. Localize o arquivo `index.html`.
3. Clique com o botão direito no arquivo.
4. Selecione **Open with Live Server**.

O frontend será aberto no navegador, normalmente em:

```text
http://127.0.0.1:5500
```

O backend e o frontend precisam permanecer em execução simultaneamente para que a interface consiga se comunicar com a API.

**Importante:** para acessar o sistema, utilize uma conta de usuário previamente cadastrada. Os scripts auxiliares de criação de usuários estão disponíveis no diretório `scripts/`.

## 11. Documentação da API

O FastAPI disponibiliza documentação interativa dos endpoints da aplicação.

Com o backend em execução, acesse:

**Swagger UI:**

http://127.0.0.1:8000/docs

**ReDoc:**

http://127.0.0.1:8000/redoc

Por meio da documentação, é possível visualizar as rotas disponíveis, consultar os parâmetros das requisições, verificar os formatos de resposta e testar operações da API.

## 12. Qualidade de software e testes

A qualidade de software foi considerada durante o desenvolvimento do EduConnect.

Foram utilizadas práticas de validação, testes automatizados e organização do código para verificar o comportamento da aplicação.

### Testes automatizados

O projeto utiliza Pytest para executar testes relacionados às funcionalidades da API e ao acesso ao banco de dados.

Para executar a suíte de testes:

```bash
py -m pytest -v
```

### Verificação de qualidade do código

O Ruff pode ser utilizado para verificar problemas de estilo e qualidade estática do código Python.

```bash
py -m ruff check .
```

### Integração contínua

O repositório utiliza GitHub Actions para executar verificações automatizadas durante o fluxo de Pull Requests.

Essa prática ajuda a identificar problemas antes que as alterações sejam integradas à branch principal de desenvolvimento.

## 13. Versionamento e colaboração

O desenvolvimento foi organizado com Git e GitHub, utilizando branches para separar as atividades e Pull Requests para revisar e integrar as alterações.

O fluxo de trabalho adotado considera:

- `main`: branch principal do projeto.
- `develop`: branch de desenvolvimento e integração.
- `feature/*`: branches destinadas à implementação de funcionalidades.
- `fix/*`: branches destinadas à correção de problemas.

As alterações são desenvolvidas em branches específicas, registradas por meio de commits e enviadas ao GitHub para revisão.

Após a aprovação e a execução das verificações necessárias, as alterações podem ser integradas à branch `develop`.

## 14. Identidade visual

O EduConnect possui uma identidade visual própria, desenvolvida para representar a proposta de gestão escolar inteligente.

A interface utiliza uma combinação de azul-marinho, amarelo, branco e tons neutros, buscando transmitir organização, clareza e facilidade de utilização.

A logomarca está presente na tela de autenticação e no menu lateral da aplicação.

## 15. Possibilidades de evolução

O projeto pode ser ampliado futuramente de acordo com as necessidades de uma instituição de ensino.

Entre as possibilidades de evolução estão:

- Implementação de relatórios acadêmicos.
- Ampliação dos filtros de consulta.
- Melhorias nos indicadores e painéis de acompanhamento.
- Aprimoramento da experiência do usuário.
- Ampliação da cobertura de testes.
- Melhorias adicionais de segurança e controle de acesso.
- Implementação de novos módulos de gestão escolar.

Esses itens representam possibilidades futuras, não necessariamente funcionalidades já entregues.

## 16. Considerações finais

O EduConnect foi desenvolvido com o propósito de demonstrar como tecnologias de desenvolvimento web, APIs REST e bancos de dados relacionais podem ser utilizadas para organizar informações escolares.

Além da implementação das funcionalidades, o projeto permitiu aplicar conhecimentos de programação, modelagem de dados, validação, testes automatizados, controle de versão e colaboração em equipe.

A aplicação reúne uma API, um banco de dados integrado e uma interface web, formando uma base que pode ser aprimorada e expandida conforme novas necessidades.

---

## 17. Integrantes do grupo

Projeto desenvolvido em equipe para a disciplina de **Gestão e Qualidade de Software**.

- **Gabriel Gobira**
- **Marcella Anataniel**
- **Nathaly Caroline**
- **William Lázaro**

---

<p align="center">
  <strong>EduConnect — Gestão Escolar Inteligente</strong>
  <br>
  Projeto acadêmico • 2026
</p>