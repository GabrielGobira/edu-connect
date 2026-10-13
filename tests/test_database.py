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