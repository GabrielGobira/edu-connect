from app.database import Base, engine
from app import models


def criar_banco():
    # Garante que os modelos sejam carregados
    # antes da criação das tabelas.
    _ = models.Usuario
    _ = models.Aluno
    _ = models.Nota
    _ = models.Frequencia
    _ = models.Ocorrencia

    Base.metadata.create_all(bind=engine)

    print("Banco de dados e tabelas criados com sucesso!")


if __name__ == "__main__":
    criar_banco()
