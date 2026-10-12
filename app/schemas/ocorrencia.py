
from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OcorrenciaCreate(BaseModel):
    aluno_id: int = Field(gt=0)
    descricao: str = Field(min_length=1, max_length=500)
    data: date

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, valor: str) -> str:
        valor = valor.strip()

        if not valor:
            raise ValueError("A descrição da ocorrência não pode ficar vazia.")

        return valor

class OcorrenciaResponse(BaseModel):
    id: int
    aluno_id: int
    descricao: str
    data: date

    model_config = ConfigDict(from_attributes=True)

