
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
import app.main as modulo_principal
import app.models

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
    db = SessaoTeste()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def preparar_banco():
    override_anterior = app.dependency_overrides.get(get_db)

    app.dependency_overrides[get_db] = substituir_banco

    Base.metadata.drop_all(bind=engine_teste)
    Base.metadata.create_all(bind=engine_teste)

    yield

    Base.metadata.drop_all(bind=engine_teste)

    if override_anterior is None:
        app.dependency_overrides.pop(get_db, None)
    else:
        app.dependency_overrides[get_db] = override_anterior


client = TestClient(app)


def cadastrar_aluno_teste():
    return client.post(
        "/alunos",
        json={
            "nome": "Ana Silva",
            "matricula": "2026004",
            "turma": "ADS-01"
        }
    )


def test_cadastrar_frequencia():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    resposta = client.post(
        "/frequencias",
        json={
            "aluno_id": aluno_id,
            "data": "2026-10-12",
            "presente": True
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["aluno_id"] == aluno_id
    assert resposta.json()["data"] == "2026-10-12"
    assert resposta.json()["presente"] is True


def test_cadastrar_frequencia_para_aluno_inexistente():
    resposta = client.post(
        "/frequencias",
        json={
            "aluno_id": 99999,
            "data": "2026-10-12",
            "presente": True
        }
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Aluno não encontrado."


def test_rejeitar_frequencia_duplicada():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    dados = {
        "aluno_id": aluno_id,
        "data": "2026-10-12",
        "presente": True
    }

    primeira_resposta = client.post(
        "/frequencias",
        json=dados
    )

    segunda_resposta = client.post(
        "/frequencias",
        json=dados
    )

    assert primeira_resposta.status_code == 201
    assert segunda_resposta.status_code == 409


def test_listar_frequencias():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    client.post(
        "/frequencias",
        json={
            "aluno_id": aluno_id,
            "data": "2026-10-12",
            "presente": True
        }
    )

    resposta = client.get("/frequencias")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["aluno_id"] == aluno_id


def test_filtrar_frequencias_por_aluno():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    client.post(
        "/frequencias",
        json={
            "aluno_id": aluno_id,
            "data": "2026-10-12",
            "presente": False
        }
    )

    resposta = client.get(
        "/frequencias",
        params={"aluno_id": aluno_id}
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["aluno_id"] == aluno_id
    assert resposta.json()[0]["presente"] is False
