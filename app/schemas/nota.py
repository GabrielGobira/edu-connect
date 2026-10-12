
from pydantic import BaseModel, ConfigDict, Field


class NotaCreate(BaseModel):
    aluno_id: int = Field(gt=0)
    disciplina: str = Field(min_length=1, max_length=100)
    nota: float = Field(ge=0, le=10)


class NotaResponse(BaseModel):
    id: int
    aluno_id: int
    disciplina: str
    nota: float

    model_config = ConfigDict(from_attributes=True)
