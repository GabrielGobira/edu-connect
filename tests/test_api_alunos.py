
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import app.models
from app.database import Base, get_db
import app.main as modulo_principal

app = modulo_principal.app



engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

SessaoTeste = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_teste
)


def substituir_banco():
    Base.metadata.create_all(bind=engine_teste)
    db = SessaoTeste()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = substituir_banco


@pytest.fixture(autouse=True)
def preparar_banco():
    Base.metadata.drop_all(bind=engine_teste)
    Base.metadata.create_all(bind=engine_teste)
    yield
    Base.metadata.drop_all(bind=engine_teste)


client = TestClient(app)


def test_rota_inicial():
    resposta = client.get("/")

    assert resposta.status_code == 200
    assert resposta.json() == {
        "mensagem": "Bem-vindo ao EduConnect"
    }


def test_cadastrar_aluno():
    resposta = client.post(
        "/alunos",
        json={
            "nome": "Ana Silva",
            "matricula": "2026004",
            "turma": "ADS-01"
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["nome"] == "Ana Silva"
    assert resposta.json()["matricula"] == "2026004"
    assert resposta.json()["turma"] == "ADS-01"
    assert "id" in resposta.json()


def test_matricula_duplicada():
    dados = {
        "nome": "Ana Silva",
        "matricula": "2026004",
        "turma": "ADS-01"
    }

    primeira_resposta = client.post("/alunos", json=dados)
    segunda_resposta = client.post("/alunos", json=dados)

    assert primeira_resposta.status_code == 201
    assert segunda_resposta.status_code == 409


def test_cadastrar_aluno_com_dados_invalidos():
    resposta = client.post(
        "/alunos",
        json={
            "nome": "",
            "matricula": "2026005",
            "turma": "ADS-01"
        }
    )

    assert resposta.status_code == 422


def test_listar_alunos():
    client.post(
        "/alunos",
        json={
            "nome": "Ana Silva",
            "matricula": "2026004",
            "turma": "ADS-01"
        }
    )

    resposta = client.get("/alunos")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["nome"] == "Ana Silva"

def test_buscar_aluno_existente():
    client.post(
        "/alunos",
        json={
            "nome": "Ana Silva",
            "matricula": "2026004",
            "turma": "ADS-01"
        }
    )

    resposta = client.get("/alunos/1")

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Ana Silva"


def test_buscar_aluno_inexistente():
    resposta = client.get("/alunos/99999")

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Aluno não encontrado."

    
def test_atualizar_aluno():
    cadastro = client.post(
        "/alunos",
        json={
            "nome": "Ana Silva",
            "matricula": "2026004",
            "turma": "ADS-01"
        }
    )

    aluno_id = cadastro.json()["id"]

    resposta = client.put(
        f"/alunos/{aluno_id}",
        json={
            "nome": "Ana Souza",
            "matricula": "2026004",
            "turma": "ADS-02"
        }
    )

    assert resposta.status_code == 200
    assert resposta.json()["nome"] == "Ana Souza"
    assert resposta.json()["turma"] == "ADS-02"


def test_atualizar_aluno_inexistente():
    resposta = client.put(
        "/alunos/99999",
        json={
            "nome": "Ana Souza",
            "matricula": "2026005",
            "turma": "ADS-02"
        }
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Aluno não encontrado."


def test_atualizar_com_matricula_duplicada():
    primeiro = client.post(
        "/alunos",
        json={
            "nome": "Ana Silva",
            "matricula": "2026004",
            "turma": "ADS-01"
        }
    )

    segundo = client.post(
        "/alunos",
        json={
            "nome": "Bruno Souza",
            "matricula": "2026005",
            "turma": "ADS-01"
        }
    )

    aluno_id = segundo.json()["id"]

    resposta = client.put(
        f"/alunos/{aluno_id}",
        json={
            "nome": "Bruno Souza",
            "matricula": "2026004",
            "turma": "ADS-02"
        }
    )

    assert primeiro.status_code == 201
    assert segundo.status_code == 201
    assert resposta.status_code == 409
    assert resposta.json()["detail"] == (
        "Já existe outro aluno com essa matrícula."
    )
