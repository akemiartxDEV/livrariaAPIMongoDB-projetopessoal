from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from bson import ObjectId
from bson.errors import InvalidId
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field, ConfigDict
from database import livros, usuarios

app = FastAPI(
    title="API Biblioteca",
    description="API de estudo para registrar livros, usuários e empréstimos de uma biblioteca.",
    version="0.1.0",
)

def converter_id(livro_id: str) -> ObjectId:
    try:
        return ObjectId(livro_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

@app.get("/")
def raiz():
    return {"mensagem": "API da biblioteca funcionando"}


@app.get("/livros")
def listar_livros():
    lista = []
    for livro in livros.find():
        livro["_id"] = str(livro["_id"])
        lista.append(livro)
    return lista

class LivroNovo(BaseModel):
    titulo: str
    autor: str
    ano: int
    exemplares: int = 1


@app.post("/livros", status_code=201)
def cadastrar_livro(livro: LivroNovo):
    documento = livro.model_dump()
    documento["disponivel"] = documento["exemplares"] > 0
    resultado = livros.insert_one(documento)
    return {"mensagem": "Livro cadastrado com sucesso", "id": str(resultado.inserted_id)}

@app.get("/livros/{livro_id}")
def buscar_livro(livro_id: str):
    objeto_id = converter_id(livro_id)

    livro = livros.find_one({"_id": objeto_id})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    livro["_id"] = str(livro["_id"])
    return livro

class LivroAtualizacao(BaseModel):
    titulo: Optional[str] = None
    autor: Optional[str] = None
    ano: Optional[int] = None
    exemplares: Optional[int] = Field(default=None, ge=0)


@app.patch("/livros/{livro_id}")
def atualizar_livro(livro_id: str, dados: LivroAtualizacao):
    objeto_id = converter_id(livro_id)

    campos = dados.model_dump(exclude_unset=True, exclude_none=True)
    if not campos:
        raise HTTPException(status_code=400, detail="Nenhum campo enviado para atualizar")

    if "exemplares" in campos:
        campos["disponivel"] = campos["exemplares"] > 0

    resultado = livros.update_one({"_id": objeto_id}, {"$set": campos})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    livro = livros.find_one({"_id": objeto_id})
    livro["_id"] = str(livro["_id"])
    return livro

@app.delete("/livros/{livro_id}")
def remover_livro(livro_id: str):
    objeto_id = converter_id(livro_id)

    resultado = livros.delete_one({"_id": objeto_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    return {"mensagem": "Livro removido com sucesso"}

class UsuarioNovo(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    nome: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=100)


@app.post("/usuarios", status_code=201)
def cadastrar_usuario(usuario: UsuarioNovo):
    email = usuario.email.strip().lower()

    if usuarios.find_one({"email": email}):
        raise HTTPException(status_code=409, detail="Já existe um usuário com esse e-mail")

    documento = {
        "nome": usuario.nome.strip(),
        "email": email,
        "data_cadastro": datetime.now(timezone.utc),
    }
    resultado = usuarios.insert_one(documento)
    return {"mensagem": "Usuário cadastrado com sucesso", "id": str(resultado.inserted_id)}


@app.get("/usuarios")
def listar_usuarios():
    lista = []
    for usuario in usuarios.find():
        usuario["_id"] = str(usuario["_id"])
        lista.append(usuario)
    return lista