import os
os.environ["EDUCONNECT_JWT_SECRET"] = "chave-exclusiva-para-testes-automatizados"
from fastapi.testclient import TestClient
from app.security import criar_token, gerar_hash_senha, verificar_senha
from app.models.usuario import Usuario
from app.database import get_db
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import app.models
from app.database import Base
from app.main import app
from datetime import datetime, timedelta, timezone
import jwt
from app.security import ALGORITHM, decodificar_token
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError

engine_teste = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessaoTeste = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_teste,
)


def substituir_banco():
    db = SessaoTeste()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def preparar_banco():
    app.dependency_overrides[get_db] = substituir_banco

    Base.metadata.drop_all(bind=engine_teste)
    Base.metadata.create_all(bind=engine_teste)

    yield

    Base.metadata.drop_all(bind=engine_teste)
    app.dependency_overrides.pop(get_db, None)

client = TestClient(app)


def test_excluir_aluno_sem_token():
    resposta = client.delete("/alunos/1")

    assert resposta.status_code == 401

def test_excluir_aluno_com_token_invalido():
    resposta = client.delete(
        "/alunos/1",
        headers={
            "Authorization": "Bearer token_falso"
        }
    )

    assert resposta.status_code == 401
    assert resposta.json()["detail"] == (
        "Token inválido ou expirado."
    )
def test_criar_token_jwt_valido():
    token = criar_token(usuario_id=1)

    assert isinstance(token, str)
    assert len(token) > 0
def test_usuario_comum_nao_pode_excluir_aluno():
    db = next(app.dependency_overrides[get_db]())

    try:
        usuario = Usuario(
            nome="Usuario Teste",
            email="usuario.teste@example.com",
            senha="hash_ficticio",
            tipo="professor",
        )

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        token = criar_token(usuario.id)

        resposta = client.delete(
            "/alunos/1",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert resposta.status_code == 403

    finally:
        db.close()

def test_admin_excluir_aluno_inexistente():
    db = SessaoTeste()

    try:
        administrador = Usuario(
            nome="Administrador Teste",
            email="admin.teste@example.com",
            senha="hash_ficticio",
            tipo="admin",
        )

        db.add(administrador)
        db.commit()
        db.refresh(administrador)

        token = criar_token(administrador.id)

        resposta = client.delete(
            "/alunos/99999",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert resposta.status_code == 404
        assert resposta.json()["detail"] == (
            "Aluno não encontrado."
        )

    finally:
        db.close()

def test_admin_excluir_aluno_com_sucesso():
    db = SessaoTeste()

    try:
        administrador = Usuario(
            nome="Administrador Teste",
            email="admin.exclusao@example.com",
            senha="hash_ficticio",
            tipo="admin",
        )

        db.add(administrador)
        db.commit()
        db.refresh(administrador)

        token = criar_token(administrador.id)

        cadastro = client.post(
            "/alunos",
            json={
                "nome": "Aluno Teste Exclusao",
                "matricula": "TESTE-DELETE-001",
                "turma": "ADS-01",
            },
        )

        assert cadastro.status_code == 201

        aluno_id = cadastro.json()["id"]

        resposta = client.delete(
            f"/alunos/{aluno_id}",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert resposta.status_code == 204

        consulta = client.get(f"/alunos/{aluno_id}")

        assert consulta.status_code == 404

    finally:
        db.close()

def test_admin_nao_pode_excluir_aluno_com_nota():
    db = SessaoTeste()

    try:
        administrador = Usuario(
            nome="Administrador Teste",
            email="admin.nota@example.com",
            senha="hash_ficticio",
            tipo="admin",
        )

        db.add(administrador)
        db.commit()
        db.refresh(administrador)

        token = criar_token(administrador.id)

        cadastro = client.post(
            "/alunos",
            json={
                "nome": "Aluno Com Nota",
                "matricula": "TESTE-DELETE-002",
                "turma": "ADS-01",
            },
        )

        assert cadastro.status_code == 201
        aluno_id = cadastro.json()["id"]

        nota = client.post(
            "/notas",
            json={
                "aluno_id": aluno_id,
                "disciplina": "Matemática",
                "nota": 8.5,
            },
        )

        assert nota.status_code == 201

        resposta = client.delete(
            f"/alunos/{aluno_id}",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert resposta.status_code == 409

        consulta = client.get(f"/alunos/{aluno_id}")
        assert consulta.status_code == 200

    finally:
        db.close()

def test_admin_nao_pode_excluir_aluno_com_frequencia():
    db = SessaoTeste()

    try:
        administrador = Usuario(
            nome="Administrador Teste",
            email="admin.frequencia@example.com",
            senha="hash_ficticio",
            tipo="admin",
        )

        db.add(administrador)
        db.commit()
        db.refresh(administrador)

        token = criar_token(administrador.id)

        cadastro = client.post(
            "/alunos",
            json={
                "nome": "Aluno Com Frequencia",
                "matricula": "TESTE-DELETE-003",
                "turma": "ADS-01",
            },
        )

        assert cadastro.status_code == 201
        aluno_id = cadastro.json()["id"]

        frequencia = client.post(
            "/frequencias",
            json={
                "aluno_id": aluno_id,
                "data": "2026-10-27",
                "presente": True,
            },
        )

        assert frequencia.status_code == 201

        resposta = client.delete(
            f"/alunos/{aluno_id}",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert resposta.status_code == 409

        consulta = client.get(f"/alunos/{aluno_id}")
        assert consulta.status_code == 200

    finally:
        db.close()

def test_admin_nao_pode_excluir_aluno_com_ocorrencia():
    db = SessaoTeste()

    try:
        administrador = Usuario(
            nome="Administrador Teste",
            email="admin.ocorrencia@example.com",
            senha="hash_ficticio",
            tipo="admin",
        )

        db.add(administrador)
        db.commit()
        db.refresh(administrador)

        token = criar_token(administrador.id)

        cadastro = client.post(
            "/alunos",
            json={
                "nome": "Aluno Com Ocorrencia",
                "matricula": "TESTE-DELETE-004",
                "turma": "ADS-01",
            },
        )

        assert cadastro.status_code == 201
        aluno_id = cadastro.json()["id"]

        ocorrencia = client.post(
            "/ocorrencias",
            json={
                "aluno_id": aluno_id,
                "descricao": "Aluno chegou atrasado à aula.",
                "data": "2026-10-27",
            },
        )

        assert ocorrencia.status_code == 201

        resposta = client.delete(
            f"/alunos/{aluno_id}",
            headers={
                "Authorization": f"Bearer {token}"
            },
        )

        assert resposta.status_code == 409

        consulta = client.get(f"/alunos/{aluno_id}")
        assert consulta.status_code == 200

    finally:
        db.close()

def test_verificar_senha_correta_e_incorreta():
    senha_original = "SenhaTeste123!"

    senha_hash = gerar_hash_senha(senha_original)

    assert verificar_senha(senha_original, senha_hash) is True

    assert verificar_senha("SenhaErrada123!", senha_hash) is False

def test_token_jwt_expirado():
    token_expirado = jwt.encode(
        {
            "sub": "1",
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        os.environ["EDUCONNECT_JWT_SECRET"],
        algorithm=ALGORITHM,
    )

    with pytest.raises(jwt.ExpiredSignatureError):
        decodificar_token(token_expirado)

def test_criar_token_sem_chave_secreta(monkeypatch):
    monkeypatch.delenv("EDUCONNECT_JWT_SECRET", raising=False)

    with pytest.raises(
        RuntimeError,
        match="EDUCONNECT_JWT_SECRET não configurada",
    ):
        criar_token(usuario_id=1)

def test_decodificar_token_sem_chave_secreta(monkeypatch):
    token = criar_token(usuario_id=1)

    monkeypatch.delenv("EDUCONNECT_JWT_SECRET", raising=False)

    with pytest.raises(
        RuntimeError,
        match="EDUCONNECT_JWT_SECRET não configurada",
    ):
        decodificar_token(token)

def test_erro_integridade_ao_excluir_aluno():
    db = SessaoTeste()

    try:
        administrador = Usuario(
            nome="Administrador Teste",
            email="admin.erro@example.com",
            senha="hash_ficticio",
            tipo="admin",
        )

        db.add(administrador)
        db.commit()
        db.refresh(administrador)

        token = criar_token(administrador.id)

        cadastro = client.post(
            "/alunos",
            json={
                "nome": "Aluno Teste Erro",
                "matricula": "TESTE-DELETE-005",
                "turma": "ADS-01",
            },
        )

        assert cadastro.status_code == 201
        aluno_id = cadastro.json()["id"]

        with patch(
            "app.main.Session.commit",
            side_effect=IntegrityError(
                "DELETE",
                {},
                Exception("erro simulado"),
            ),
        ):
            resposta = client.delete(
                f"/alunos/{aluno_id}",
                headers={
                    "Authorization": f"Bearer {token}"
                },
            )

        assert resposta.status_code == 409
        assert resposta.json()["detail"] == (
            "Não foi possível excluir o aluno devido a registros vinculados."
        )

        consulta = client.get(f"/alunos/{aluno_id}")
        assert consulta.status_code == 200

    finally:
        db.close()
