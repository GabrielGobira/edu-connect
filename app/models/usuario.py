from sqlalchemy import Column, Integer, String, CheckConstraint

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (
        CheckConstraint(
            "tipo IN ('admin', 'professor')",
            name="ck_usuario_tipo"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(String(30), nullable=False)
