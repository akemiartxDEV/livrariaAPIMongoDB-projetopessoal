from fastapi import APIRouter, HTTPException

from database import livros
from schemas import LivroNovo, LivroAtualizacao
from utils import converter_id

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.get("")
def listar_livros():
    lista = []
    for livro in livros.find():
        livro["_id"] = str(livro["_id"])
        lista.append(livro)
    return lista


@router.post("", status_code=201)
def cadastrar_livro(livro: LivroNovo):
    documento = livro.model_dump()
    documento["disponivel"] = documento["exemplares"] > 0
    resultado = livros.insert_one(documento)
    return {"mensagem": "Livro cadastrado com sucesso", "id": str(resultado.inserted_id)}


@router.get("/{livro_id}")
def buscar_livro(livro_id: str):
    objeto_id = converter_id(livro_id)
    livro = livros.find_one({"_id": objeto_id})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    livro["_id"] = str(livro["_id"])
    return livro


@router.patch("/{livro_id}")
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


@router.delete("/{livro_id}")
def remover_livro(livro_id: str):
    objeto_id = converter_id(livro_id)
    resultado = livros.delete_one({"_id": objeto_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return {"mensagem": "Livro removido com sucesso"}