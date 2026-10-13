from sqlalchemy import (
    CheckConstraint,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
)

from app.database import Base


class Nota(Base):
    __tablename__ = "notas"

    __table_args__ = (
        CheckConstraint(
            "nota >= 0 AND nota <= 10",
            name="ck_nota_intervalo",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    aluno_id = Column(
        Integer,
        ForeignKey("alunos.id"),
        nullable=False
    )

    disciplina = Column(String(100), nullable=False)

    nota = Column(Float, nullable=False)