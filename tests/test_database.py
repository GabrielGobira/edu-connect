import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.aluno import Aluno
from app.models.nota import Nota
from app.models.frequencia import Frequencia
from datetime import date
from app.models.usuario import Usuario
from app.models.ocorrencia import Ocorrencia

import app.models
from sqlalchemy import create_engine, inspect
from sqlalchemy.pool import StaticPool
from sqlalchemy.exc import IntegrityError

from app.database import Base
import app.models

from sqlalchemy import event
def criar_engine_teste():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    @event.listens_for(engine, "connect")
    def ativar_chaves_estrangeiras(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    return engine




def test_criacao_tabelas():
    engine = criar_engine_teste()
    with engine.connect() as conexao:
        resultado = conexao.exec_driver_sql("PRAGMA foreign_keys").scalar()
    assert resultado == 1

    Base.metadata.create_all(bind=engine)

    tabelas = inspect(engine).get_table_names()

    assert "usuarios" in tabelas
    assert "alunos" in tabelas
    assert "notas" in tabelas
    assert "frequencias" in tabelas
    assert "ocorrencias" in tabelas

    engine.dispose()


from sqlalchemy.orm import Session
from app.models.aluno import Aluno


def test_cadastrar_aluno():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome="Gabriel",
            matricula="2026001",
            turma="ADS-01"
        )

        session.add(aluno)
        session.commit()

        aluno_salvo = session.query(Aluno).filter_by(
            matricula="2026001"
        ).first()

        assert aluno_salvo is not None
        assert aluno_salvo.nome == "Gabriel"
        assert aluno_salvo.turma == "ADS-01"

    engine.dispose()

from sqlalchemy.exc import IntegrityError


def test_matricula_duplicada():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno1 = Aluno(
            nome="Gabriel",
            matricula="2026001",
            turma="ADS-01"
        )

        aluno2 = Aluno(
            nome="Joao",
            matricula="2026001",
            turma="ADS-02"
        )

        session.add(aluno1)
        session.commit()

        session.add(aluno2)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()
@pytest.mark.parametrize(
    "nome, matricula, disciplina, valor",
    [
        ("Gabriel", "2026001", "Matematica", 8.5),
        ("Joao", "2026002", "Portugues", 7.0),
        ("Maria", "2026003", "Historia", 9.5),
    ]
)
def test_cadastrar_nota_aluno(nome, matricula, disciplina, valor):
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome=nome,
            matricula=matricula,
            turma="ADS-01"
        )

        session.add(aluno)
        session.commit()

        nota = Nota(
            aluno_id=aluno.id,
            disciplina=disciplina,
            nota=valor
        )

        session.add(nota)
        session.commit()

        nota_salva = session.query(Nota).filter_by(
            aluno_id=aluno.id
        ).first()

        assert nota_salva is not None
        assert nota_salva.disciplina == disciplina
        assert nota_salva.nota == valor
        assert nota_salva.aluno_id == aluno.id

    engine.dispose()
    
def test_nota_aluno_inexistente():
    engine = criar_engine_teste()

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        nota = Nota(
            aluno_id=9999,
            disciplina="Matematica",
            nota=8.5
        )

        session.add(nota)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()

def test_frequencia_duplicada_no_banco():
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome="Marcella",
            matricula="2026999",
            turma="ADS-01"
        )

        session.add(aluno)
        session.commit()

        frequencia1 = Frequencia(
            aluno_id=aluno.id,
            data=date(2026, 10, 12),
            presente=True
        )

        session.add(frequencia1)
        session.commit()

        frequencia2 = Frequencia(
            aluno_id=aluno.id,
            data=date(2026, 10, 12),
            presente=False
        )

        session.add(frequencia2)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()

def test_email_usuario_duplicado():
    engine = criar_engine_teste()

    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        usuario1 = Usuario(
            nome="Gabriel",
            email="gabriel@email.com",
            senha="hash_teste_1",
            tipo="professor"
        )

        usuario2 = Usuario(
            nome="Joao",
            email="gabriel@email.com",
            senha="hash_teste_2",
            tipo="professor"
        )

        session.add(usuario1)
        session.commit()

        session.add(usuario2)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()

@pytest.mark.parametrize(
    "campo",
    ["nome", "email", "senha", "tipo"]
)
def test_campos_obrigatorios_usuario(campo):
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    dados = {
        "nome": "Gabriel",
        "email": "gabriel@email.com",
        "senha": "hash_teste",
        "tipo": "professor"
    }

    dados[campo] = None

    with Session(engine) as session:
        usuario = Usuario(**dados)
        session.add(usuario)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()
@pytest.mark.parametrize(
    "valor_nota",
    [-1.0, 10.1, 15.0]
)
def test_nota_fora_intervalo_no_banco(valor_nota):
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome="Gabriel",
            matricula="2026001",
            turma="3A"
        )

        session.add(aluno)
        session.commit()

        nota = Nota(
            aluno_id=aluno.id,
            disciplina="Matematica",
            nota=valor_nota
        )

        session.add(nota)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()
@pytest.mark.parametrize(
    "valor_nota",
    [0.0, 5.5, 10.0]
)
def test_nota_valida_no_banco(valor_nota):
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome="Gabriel",
            matricula="2026001",
            turma="3A"
        )

        session.add(aluno)
        session.commit()

        nota = Nota(
            aluno_id=aluno.id,
            disciplina="Matematica",
            nota=valor_nota
        )

        session.add(nota)
        session.commit()

        assert nota.id is not None
        assert nota.nota == valor_nota

    engine.dispose()
    
@pytest.mark.parametrize(
    "campo",
    ["aluno_id", "descricao", "data"]
)
def test_campos_obrigatorios_ocorrencia(campo):
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    dados = {
        "aluno_id": 1,
        "descricao": "Aluno chegou atrasado",
        "data": date(2026, 10, 13)
    }

    dados[campo] = None

    with Session(engine) as session:
        ocorrencia = Ocorrencia(**dados)
        session.add(ocorrencia)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()
    
@pytest.mark.parametrize(
    "campo",
    ["aluno_id", "data", "presente"]
)
def test_campos_obrigatorios_frequencia(campo):
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        dados = {
            "aluno_id": 1,
            "data": date(2026, 10, 13),
            "presente": True
        }

        dados[campo] = None

        frequencia = Frequencia(**dados)
        session.add(frequencia)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()
def test_impedir_exclusao_aluno_com_nota():
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome="Aluno Teste Exclusao",
            matricula="EXCLUSAO001",
            turma="1A"
        )

        session.add(aluno)
        session.commit()

        nota = Nota(
            aluno_id=aluno.id,
            disciplina="Matematica",
            nota=8.5
        )

        session.add(nota)
        session.commit()

        with pytest.raises(IntegrityError):
            session.delete(aluno)
            session.commit()

        session.rollback()

        assert session.get(Aluno, aluno.id) is not None

    engine.dispose()
def test_impedir_exclusao_aluno_com_frequencia():
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome="Aluno Teste Frequencia",
            matricula="EXCLUSAO002",
            turma="1A"
        )

        session.add(aluno)
        session.commit()

        aluno_id = aluno.id

        frequencia = Frequencia(
            aluno_id=aluno_id,
            data=date(2026, 10, 15),
            presente=True
        )

        session.add(frequencia)
        session.commit()

        with pytest.raises(IntegrityError):
            session.delete(aluno)
            session.commit()

        session.rollback()

        assert session.get(Aluno, aluno_id) is not None

    engine.dispose()
def test_impedir_exclusao_aluno_com_ocorrencia():
    engine = criar_engine_teste()
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        aluno = Aluno(
            nome="Aluno Teste",
            matricula="MAT-OCOR-001",
            turma="Turma A"
        )
        session.add(aluno)
        session.commit()

        ocorrencia = Ocorrencia(
            aluno_id=aluno.id,
            descricao="Ocorrência de teste",
            data=date(2026, 10, 15)
        )
        session.add(ocorrencia)
        session.commit()

        session.delete(aluno)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()

    engine.dispose()


from unittest.mock import MagicMock

from app.database import get_db


def test_get_db_fecha_sessao_ao_finalizar():
    sessao_falsa = MagicMock()

    def criar_sessao():
        return sessao_falsa

    from app import database

    sessao_original = database.SessionLocal
    database.SessionLocal = criar_sessao

    try:
        gerador = get_db()
        sessao_recebida = next(gerador)

        assert sessao_recebida is sessao_falsa

        gerador.close()

        sessao_falsa.close.assert_called_once()
    finally:
        database.SessionLocal = sessao_original

def test_criar_banco_cria_tabelas_e_exibe_mensagem(
    monkeypatch,
    capsys,
):
    from app import init_db

    chamadas = []

    def criar_tabelas_falso(bind):
        chamadas.append(bind)

    monkeypatch.setattr(
        init_db.Base.metadata,
        "create_all",
        criar_tabelas_falso,
    )

    init_db.criar_banco()

    saida = capsys.readouterr()

    assert chamadas == [init_db.engine]
    assert (
        saida.out.strip()
        == "Banco de dados e tabelas criados com sucesso!"
    )
