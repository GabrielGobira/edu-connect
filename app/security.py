import os
from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()


def gerar_hash_senha(senha: str) -> str:
    return password_hash.hash(senha)


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)


def criar_token(usuario_id: int) -> str:
    chave_secreta = os.environ.get("EDUCONNECT_JWT_SECRET")

    if not chave_secreta:
        raise RuntimeError("EDUCONNECT_JWT_SECRET não configurada.")

    expiracao = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados = {
        "sub": str(usuario_id),
        "exp": expiracao,
    }

    return jwt.encode(dados, chave_secreta, algorithm=ALGORITHM)


def decodificar_token(token: str) -> dict:
    chave_secreta = os.environ.get("EDUCONNECT_JWT_SECRET")

    if not chave_secreta:
        raise RuntimeError("EDUCONNECT_JWT_SECRET não configurada.")

    return jwt.decode(
        token,
        chave_secreta,
        algorithms=[ALGORITHM],
        options={"require": ["sub", "exp"]},
    )