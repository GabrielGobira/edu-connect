from app.database import Base, engine
from app.models import (
    Usuario,
    Aluno,
    Nota,
    Frequencia,
    Ocorrencia,
)


def criar_banco():
    Base.metadata.create_all(bind=engine)
    print("Banco de dados e tabelas criados com sucesso!")


if __name__ == "__main__":
    criar_banco()