from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from database import usuarios
from schemas import UsuarioNovo

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.post("", status_code=201)
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


@router.get("")
def listar_usuarios():
    lista = []
    for usuario in usuarios.find():
        usuario["_id"] = str(usuario["_id"])
        lista.append(usuario)
    return lista