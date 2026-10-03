from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class LivroNovo(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=100)
    ano: int
    exemplares: int = Field(default=1, ge=0)

class LivroAtualizacao(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    titulo: Optional[str] = Field(default=None, min_length=1, max_length=200)
    autor: Optional[str] = Field(default=None, min_length=1, max_length=100)
    ano: Optional[int] = None
    exemplares: Optional[int] = Field(default=None, ge=0)

class UsuarioNovo(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)