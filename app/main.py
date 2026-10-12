
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.aluno import Aluno
from app.schemas.aluno import AlunoCreate, AlunoResponse, AlunoUpdate
from app.models.nota import Nota
from app.schemas.nota import NotaCreate, NotaResponse

app = FastAPI(
    title="EduConnect",
    description="API para gerenciamento escolar",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo ao EduConnect"
    }


@app.post(
    "/alunos",
    response_model=AlunoResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_aluno(
    dados: AlunoCreate,
    db: Session = Depends(get_db)
):
    aluno_existente = db.query(Aluno).filter(
        Aluno.matricula == dados.matricula
    ).first()

    if aluno_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um aluno com essa matrícula."
        )

    aluno = Aluno(
        nome=dados.nome,
        matricula=dados.matricula,
        turma=dados.turma
    )

    try:
        db.add(aluno)
        db.commit()
        db.refresh(aluno)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível cadastrar o aluno. Verifique se a matrícula já existe."
        )

    return aluno


@app.get("/alunos", response_model=list[AlunoResponse])
def listar_alunos(db: Session = Depends(get_db)):
    return db.query(Aluno).order_by(Aluno.nome.asc()).all()

@app.get("/alunos/{aluno_id}", response_model=AlunoResponse)
def buscar_aluno(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id
    ).first()

    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado."
        )

    return aluno


@app.put("/alunos/{aluno_id}", response_model=AlunoResponse)
def atualizar_aluno(
    aluno_id: int,
    dados: AlunoUpdate,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(
        Aluno.id == aluno_id
    ).first()

    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado."
        )

    matricula_existente = db.query(Aluno).filter(
        Aluno.matricula == dados.matricula,
        Aluno.id != aluno_id
    ).first()

    if matricula_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe outro aluno com essa matrícula."
        )

    aluno.nome = dados.nome
    aluno.matricula = dados.matricula
    aluno.turma = dados.turma

    try:
        db.commit()
        db.refresh(aluno)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não foi possível atualizar o aluno."
        )

    return aluno


@app.post(
    "/notas",
    response_model=NotaResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_nota(
    dados: NotaCreate,
    db: Session = Depends(get_db)
):
    aluno = db.query(Aluno).filter(
        Aluno.id == dados.aluno_id
    ).first()

    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado."
        )

    nota = Nota(
        aluno_id=dados.aluno_id,
        disciplina=dados.disciplina,
        nota=dados.nota
    )

    db.add(nota)

    try:
        db.commit()
        db.refresh(nota)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível cadastrar a nota."
        )

    return nota


@app.get("/notas", response_model=list[NotaResponse])
def listar_notas(
    aluno_id: int | None = None,
    db: Session = Depends(get_db)
):
    consulta = db.query(Nota)

    if aluno_id is not None:
        consulta = consulta.filter(Nota.aluno_id == aluno_id)

    return consulta.order_by(Nota.id.asc()).all()
