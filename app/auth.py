
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.security import decodificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def obter_usuario_atual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    erro_autenticacao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        dados = decodificar_token(token)
        usuario_id = int(dados["sub"])
    except (jwt.InvalidTokenError, ValueError, TypeError, KeyError):
        raise erro_autenticacao

    usuario = db.query(Usuario).filter(
        Usuario.id == usuario_id
    ).first()

    if usuario is None:
        raise erro_autenticacao

    return usuario


def exigir_administrador(
    usuario: Usuario = Depends(obter_usuario_atual),
):
    if usuario.tipo != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem realizar esta operação.",
        )

    return usuario
