from fastapi import APIRouter, status, HTTPException
from pymongo.collection import Collection
from pydantic import Field
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from pydantic.json import ENCODERS_BY_TYPE
from pymongo.results import UpdateResult, DeleteResult

from ..database import db
from .models import *

ENCODERS_BY_TYPE[ObjectId]=str

# Create app
router = APIRouter()

# Collection
usuarios : Collection = db.usuarios

# API

@router.get("/")
def get(alias: str | None = None):
    lista: list[Usuario] = list(usuarios.find())

    if alias is not None:
        result: list[Usuario] = []
        for usuario in lista:
            usuario: Usuario = Usuario.parse_obj(usuario)
            if usuario.alias == alias:
                result.append(usuario)
        lista = result

    return lista

@router.get("/{id}")
def get_by_id(id: str) -> Usuario:
    return Usuario.parse_obj(usuarios.find_one({"_id": ObjectId(id)}))

@router.post("/")
def post(usuario: Contacto):
    inserted_user: InsertOneResult = usuarios.insert_one(usuario.dict(exclude_unset=True))
    created_user: Usuario = Usuario.parse_obj(usuarios.find_one({"_id": ObjectId(inserted_user.inserted_id)}))
    return created_user

@router.put("/{id}")
def put(id: str, usuario: Contacto):
    update_result : UpdateResult = usuarios.update_one({"_id": ObjectId(id)}, {"$set": usuario.dict(exclude_unset=True)})
    if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    updated : Usuario = Usuario.parse_obj(usuarios.find_one({"_id": ObjectId(id)}))
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str):
    delete_result: DeleteResult = usuarios.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {id} not found")
    return {"message": f"User with id {id} succesfully deleted"}
