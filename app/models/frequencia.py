from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer

from app.database import Base


class Frequencia(Base):
    __tablename__ = "frequencias"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(
        Integer,
        ForeignKey("alunos.id"),
        nullable=False
    )
    data = Column(Date, nullable=False)
    presente = Column(Boolean, nullable=False)