
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class OcorrenciaCreate(BaseModel):
    aluno_id: int = Field(gt=0)
    descricao: str = Field(min_length=1, max_length=500)
    data: date


class OcorrenciaResponse(BaseModel):
    id: int
    aluno_id: int
    descricao: str
    data: date

    model_config = ConfigDict(from_attributes=True)

