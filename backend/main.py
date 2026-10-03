from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException

from database import usuarios
from schemas import UsuarioNovo
from routers.livros import router as livros_router

app = FastAPI(
    title="API Biblioteca",
    description="API de estudo para registrar livros, usuários e empréstimos de uma biblioteca.",
    version="0.1.0",
)

app.include_router(livros_router)

@app.get("/")
def raiz():
    return {"mensagem": "API da biblioteca funcionando"}


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