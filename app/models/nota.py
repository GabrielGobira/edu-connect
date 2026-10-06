from sqlalchemy import Column, Float, ForeignKey, Integer, String

from app.database import Base


class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(
        Integer,
        ForeignKey("alunos.id"),
        nullable=False
    )
    disciplina = Column(String(100), nullable=False)
    nota = Column(Float, nullable=False)