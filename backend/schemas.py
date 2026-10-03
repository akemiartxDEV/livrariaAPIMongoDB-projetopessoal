from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class LivroNovo(BaseModel):
    titulo: str
    autor: str
    ano: int
    exemplares: int = 1

class LivroAtualizacao(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    exemplares: Optional[int] = Field(default=None, ge=0)


class UsuarioNovo(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)