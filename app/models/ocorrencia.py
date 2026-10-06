from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.database import Base


class Ocorrencia(Base):
    __tablename__ = "ocorrencias"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(
        Integer,
        ForeignKey("alunos.id"),
        nullable=False
    )
    descricao = Column(String(500), nullable=False)
    data = Column(Date, nullable=False)