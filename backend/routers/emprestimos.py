from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException

from database import livros, usuarios, emprestimos
from schemas import EmprestimoNovo
from utils import converter_id

PRAZO_DIAS = 14

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])

@router.post("", status_code=201)
def registrar_emprestimo(dados: EmprestimoNovo):
    livro_oid = converter_id(dados.livro_id)
    usuario_oid = converter_id(dados.usuario_id)

    livro = livros.find_one({"_id": livro_oid})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    if usuarios.find_one({"_id": usuario_oid}) is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    agora = datetime.now(timezone.utc)
    documento = {
        "livro_id": livro_oid,
        "usuario_id": usuario_oid,
        "data_emprestimo": agora,
        "data_prevista_devolucao": agora + timedelta(days=PRAZO_DIAS),
        "data_devolucao": None,
    }

    # Tenta reservar um exemplar sem deixar o estoque ficar negativo.
    estoque_atualizado = livros.update_one(
        {"_id": livro_oid, "exemplares": {"$gt": 1}},
        {
            "$inc": {"exemplares": -1},
            "$set": {"disponivel": True},
        },
    )

    # Se restava exatamente um exemplar, reserva esse último.
    if estoque_atualizado.modified_count == 0:
        estoque_atualizado = livros.update_one(
            {"_id": livro_oid, "exemplares": 1},
            {
                "$set": {
                    "exemplares": 0,
                    "disponivel": False,
                }
            },
        )

    if estoque_atualizado.modified_count == 0:
        raise HTTPException(
            status_code=409,
            detail="Não há exemplares disponíveis deste livro",
        )

    try:
        resultado = emprestimos.insert_one(documento)
    except Exception:
        # Se não conseguir salvar o empréstimo, devolve o exemplar ao estoque.
        livros.update_one(
            {"_id": livro_oid},
            {
                "$inc": {"exemplares": 1},
                "$set": {"disponivel": True},
            },
        )
        raise

    return {
        "mensagem": "Empréstimo registrado com sucesso",
        "id": str(resultado.inserted_id),
    }

@router.get("")
def listar_emprestimos():
    lista = []

    for emprestimo in emprestimos.find():
        emprestimo["_id"] = str(emprestimo["_id"])
        emprestimo["livro_id"] = str(emprestimo["livro_id"])
        emprestimo["usuario_id"] = str(emprestimo["usuario_id"])
        lista.append(emprestimo)
    return lista

@router.patch("/{emprestimo_id}/devolucao")
def devolver_livro(emprestimo_id: str):
    emprestimo_oid = converter_id(emprestimo_id)

    emprestimo = emprestimos.find_one({"_id": emprestimo_oid})
    if emprestimo is None:
        raise HTTPException(status_code=404, detail="Empréstimo não encontrado")

    livro = livros.find_one({"_id": emprestimo["livro_id"]})
    if livro is None:
        raise HTTPException(
            status_code=409,
            detail="O livro associado a este empréstimo não foi encontrado",
        )

    resultado = emprestimos.update_one(
        {"_id": emprestimo_oid, "data_devolucao": None},
        {"$set": {"data_devolucao": datetime.now(timezone.utc)}},
    )

    if resultado.modified_count == 0:
        raise HTTPException(
            status_code=409,
            detail="Este empréstimo já foi devolvido",
        )

    livros.update_one(
        {"_id": emprestimo["livro_id"]},
        {"$inc": {"exemplares": 1}, "$set": {"disponivel": True}},
    )

    return {"mensagem": "Devolução registrada com sucesso"}