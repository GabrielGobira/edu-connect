from getpass import getpass

from sqlalchemy.exc import IntegrityError

from app.database import SessionLocal
from app.models.usuario import Usuario
from app.security import gerar_hash_senha


def criar_admin():
    print("\n=== Cadastro do primeiro administrador ===\n")

    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()
    senha = getpass("Senha: ")
    confirmar_senha = getpass("Confirme a senha: ")

    if not nome or not email or not senha:
        print("\nPreencha todos os campos.")
        return

    if senha != confirmar_senha:
        print("\nAs senhas não conferem.")
        return

    db = SessionLocal()

    try:
        existente = (
            db.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if existente:
            print("\nJá existe um usuário com esse e-mail.")
            return

        administrador = Usuario(
            nome=nome,
            email=email,
            senha=gerar_hash_senha(senha),
            tipo="admin"
        )

        db.add(administrador)
        db.commit()
        db.refresh(administrador)

        print("\nAdministrador criado com sucesso!")
        print(f"ID: {administrador.id}")
        print(f"E-mail: {administrador.email}")

    except IntegrityError:
        db.rollback()
        print("\nNão foi possível cadastrar. Verifique se o e-mail já existe.")

    finally:
        db.close()


if __name__ == "__main__":
    criar_admin()