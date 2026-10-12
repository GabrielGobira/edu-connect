
from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class FrequenciaCreate(BaseModel):
    aluno_id: int = Field(gt=0)
    data: date
    presente: bool


class FrequenciaResponse(BaseModel):
    id: int
    aluno_id: int
    data: date
    presente: bool

    model_config = ConfigDict(from_attributes=True)

