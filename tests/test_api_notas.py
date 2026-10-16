
import pytest
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
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
    # Guarda a configuração anterior do banco de dados
    override_anterior = app.dependency_overrides.get(get_db)

    # Configura a API para utilizar o banco de teste
    app.dependency_overrides[get_db] = substituir_banco

    # Limpa e recria as tabelas antes de cada teste
    Base.metadata.drop_all(bind=engine_teste)
    Base.metadata.create_all(bind=engine_teste)

    yield

    # Limpa as tabelas após cada teste
    Base.metadata.drop_all(bind=engine_teste)

    # Restaura a configuração anterior
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


def test_cadastrar_nota():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    resposta = client.post(
        "/notas",
        json={
            "aluno_id": aluno_id,
            "disciplina": "Matemática",
            "nota": 8.5
        }
    )

    assert resposta.status_code == 201
    assert resposta.json()["aluno_id"] == aluno_id
    assert resposta.json()["disciplina"] == "Matemática"
    assert resposta.json()["nota"] == 8.5


def test_cadastrar_nota_para_aluno_inexistente():
    resposta = client.post(
        "/notas",
        json={
            "aluno_id": 99999,
            "disciplina": "Matemática",
            "nota": 8.5
        }
    )

    assert resposta.status_code == 404
    assert resposta.json()["detail"] == "Aluno não encontrado."


@pytest.mark.parametrize("nota", [-1, 10.1])
def test_rejeitar_nota_fora_do_intervalo(nota):
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    resposta = client.post(
        "/notas",
        json={
            "aluno_id": aluno_id,
            "disciplina": "Matemática",
            "nota": nota
        }
    )

    assert resposta.status_code == 422


def test_listar_notas():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    client.post(
        "/notas",
        json={
            "aluno_id": aluno_id,
            "disciplina": "Matemática",
            "nota": 8.5
        }
    )

    resposta = client.get("/notas")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["disciplina"] == "Matemática"


def test_filtrar_notas_por_aluno():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    client.post(
        "/notas",
        json={
            "aluno_id": aluno_id,
            "disciplina": "Matemática",
            "nota": 8.5
        }
    )

    resposta = client.get(
        "/notas",
        params={"aluno_id": aluno_id}
    )

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["aluno_id"] == aluno_id

def test_tratar_erro_integridade_ao_cadastrar_nota():
    aluno = cadastrar_aluno_teste()
    aluno_id = aluno.json()["id"]

    with patch(
        "app.main.Session.commit",
        side_effect=IntegrityError(
            "INSERT",
            {},
            Exception("erro simulado")
        ),
    ):
        resposta = client.post(
            "/notas",
            json={
                "aluno_id": aluno_id,
                "disciplina": "Matemática",
                "nota": 8.5
            }
        )

    assert resposta.status_code == 400
    assert resposta.json()["detail"] == "Não foi possível cadastrar a nota."

