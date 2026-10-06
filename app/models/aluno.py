from sqlalchemy import Column, Integer, String

from app.database import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    matricula = Column(String(30), unique=True, nullable=False, index=True)
    turma = Column(String(50), nullable=False)