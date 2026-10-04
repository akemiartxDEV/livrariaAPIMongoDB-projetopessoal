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
    
    if livro["exemplares"] <= 0:
        raise HTTPException(status_code=409, detail="Não há exemplares disponíveis deste livro")
    
    agora = datetime.now(timezone.utc)
    documento = {
        "livro_id": livro_oid,
        "usuario_id": usuario_oid,
        "data_emprestimo": agora,
        "data_prevista_devolucao": agora + timedelta(days=PRAZO_DIAS),
        "data_devolucao": None,
    }
    resultado = emprestimos.insert_one(documento)

    restantes = livro["exemplares"] - 1
    livros.update_one(
        {"_id": livro_oid},
        {"$inc": {"exemplares": -1}, "$set": {"disponivel": restantes > 0}},
    )

    return {"mensagem": "Empréstimo registrado com sucesso", "id": str(resultado.inserted_id)}

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

    if emprestimo["data_devolucao"] is not None:
        raise HTTPException(status_code=409, detail="Este empréstimo já foi devolvido")

    emprestimos.update_one(
        {"_id": emprestimo_oid},
        {"$set": {"data_devolucao": datetime.now(timezone.utc)}},
    )

    livros.update_one(
        {"_id": emprestimo["livro_id"]},
        {"$inc": {"exemplares": 1}, "$set": {"disponivel": True}},
    )

    return {"mensagem": "Devolução registrada com sucesso"}