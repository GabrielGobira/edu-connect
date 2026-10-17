
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    UniqueConstraint,
)

from app.database import Base


class Frequencia(Base):
    __tablename__ = "frequencias"

    __table_args__ = (
        UniqueConstraint(
            "aluno_id",
            "data",
            name="uq_frequencia_aluno_data",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(
        Integer,
        ForeignKey("alunos.id"),
        nullable=False,
    )
    data = Column(Date, nullable=False)
    presente = Column(Boolean, nullable=False)
