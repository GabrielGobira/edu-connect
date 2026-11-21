# 🎓 EduConnect

> Sistema de gestão escolar para controle de **alunos, notas, frequência e ocorrências**.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/Banco-SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/licen%C3%A7a-MIT-green)

---

## 📑 Sumário

- [Sobre o projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e execução](#-instalação-e-execução)
- [Configuração](#-configuração)
- [Modelo de dados](#-modelo-de-dados)
- [Testes](#-testes)
- [Roadmap](#-roadmap)
- [Como contribuir](#-como-contribuir)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 📖 Sobre o projeto

O **EduConnect** é um sistema de gestão escolar que centraliza as informações acadêmicas e disciplinares de uma instituição de ensino. Ele substitui planilhas e registros em papel por uma solução única, permitindo que a equipe escolar:

- cadastre e consulte alunos de forma organizada;
- lance e acompanhe notas por disciplina e período;
- registre a frequência (presenças e faltas);
- documente ocorrências disciplinares e pedagógicas;
- acompanhe o desempenho individual e da turma.

O objetivo é reduzir o trabalho manual, evitar a perda de informação e dar visibilidade rápida sobre a situação de cada aluno.

---

## ✨ Funcionalidades

| Módulo | Descrição |
| --- | --- |
| 👤 **Alunos** | Cadastro, edição, busca e inativação de alunos, com dados pessoais e de matrícula. |
| 📝 **Notas** | Lançamento de notas por disciplina e período, cálculo de médias e situação (aprovado, recuperação, reprovado). |
| 📅 **Frequência** | Registro de presença e falta por aula/dia e cálculo do percentual de frequência. |
| ⚠️ **Ocorrências** | Registro de ocorrências com data, tipo, descrição e responsável pelo registro. |
| 📊 **Relatórios** | Consulta consolidada de desempenho, frequência e histórico de cada aluno. |

---

## 🛠 Tecnologias

- **[Python](https://www.python.org/)**: linguagem principal
- **[SQLite](https://www.sqlite.org/)**: banco de dados local
- **Git e GitHub**: versionamento e colaboração

---

## 📂 Estrutura do projeto

```
edu-connect/
├── src/                  # Código-fonte da aplicação
│   ├── models/           # Entidades (Aluno, Nota, Frequência, Ocorrência)
│   ├── services/         # Regras de negócio
│   ├── database/         # Conexão e criação das tabelas
│   └── main.py           # Ponto de entrada
├── tests/                # Testes automatizados
├── .env.example          # Exemplo de variáveis de ambiente
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt      # Dependências Python
```

---

## ✅ Pré-requisitos

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- `pip` (já incluso no Python)

---

## 🚀 Instalação e execução

```bash
# 1. Clone o repositório
git clone https://github.com/GabrielGobira/edu-connect.git
cd edu-connect

# 2. Crie e ative um ambiente virtual
python -m venv venv

# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env

# 5. Execute a aplicação
python src/main.py
```

O arquivo de banco SQLite (`*.db`) é criado localmente na primeira execução e não é versionado.

---

## ⚙️ Configuração

As configurações ficam em um arquivo `.env` na raiz do projeto (ignorado pelo Git). Exemplo:

```env
# Caminho do banco de dados local
DATABASE_PATH=educonnect.db

# Ambiente: development | production
APP_ENV=development
```

Nunca faça commit do arquivo `.env`. Mantenha apenas o `.env.example`, sem valores reais.

---

## 🗄 Modelo de dados

```
ALUNO 1 ──── N NOTA
ALUNO 1 ──── N FREQUENCIA
ALUNO 1 ──── N OCORRENCIA
```

| Entidade | Campos principais |
| --- | --- |
| **Aluno** | id, nome, matrícula, data de nascimento, turma, status |
| **Nota** | id, aluno_id, disciplina, período, valor |
| **Frequência** | id, aluno_id, data, presente, observação |
| **Ocorrência** | id, aluno_id, data, tipo, descrição, registrado_por |

---

## 🧪 Testes

```bash
pip install pytest
pytest
```

Para ver a cobertura:

```bash
pip install pytest-cov
pytest --cov=src
```

---

## 🗺 Roadmap

- [x] Definição do escopo e estrutura inicial do repositório
- [ ] CRUD de alunos
- [ ] Lançamento de notas e cálculo de médias
- [ ] Controle de frequência
- [ ] Registro de ocorrências
- [ ] Relatórios por aluno e por turma
- [ ] Autenticação e perfis de acesso (professor, coordenação, secretaria)
- [ ] Exportação de relatórios (PDF/CSV)
- [ ] Testes automatizados e integração contínua (GitHub Actions)

---

## 🤝 Como contribuir

1. Faça um **fork** do projeto
2. Crie uma branch: `git checkout -b feature/minha-feature`
3. Faça commit das mudanças: `git commit -m "feat: adiciona minha feature"`
4. Envie para o seu fork: `git push origin feature/minha-feature`
5. Abra um **Pull Request**

Sugestão de padrão de commits: [Conventional Commits](https://www.conventionalcommits.org/pt-br/).

---

## 📄 Licença

Distribuído sob a licença **MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

