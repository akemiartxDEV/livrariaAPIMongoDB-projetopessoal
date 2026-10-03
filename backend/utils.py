from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException


def converter_id(id_texto: str) -> ObjectId:
    try:
        return ObjectId(id_texto)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")