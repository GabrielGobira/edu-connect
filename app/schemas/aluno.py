
from pydantic import BaseModel, ConfigDict, Field


class AlunoCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    matricula: str = Field(min_length=1, max_length=30)
    turma: str = Field(min_length=1, max_length=50)


class AlunoResponse(BaseModel):
    id: int
    nome: str
    matricula: str
    turma: str

    model_config = ConfigDict(from_attributes=True)

class AlunoUpdate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    matricula: str = Field(min_length=1, max_length=30)
    turma: str = Field(min_length=1, max_length=50)