from fastapi import APIRouter, status, HTTPException
from pymongo.collection import Collection
from pydantic import Field
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from pydantic.json import ENCODERS_BY_TYPE
from pymongo.results import UpdateResult, DeleteResult
from datetime import datetime

from ..database import db
from .models import *

ENCODERS_BY_TYPE[ObjectId]=str

# Create app
router = APIRouter()

# Collection
mensajes : Collection = db.mensajes

# API

@router.get("/")
def get(match: str):
    lista: list[Mensaje] = list(mensajes.find())

    if match is not None:
        result: list[Mensaje] = []
        for mensaje in lista:
            mensaje: Mensaje = Mensaje.parse_obj(mensaje)
            if match in mensaje.texto:
                result.append(mensaje)
        lista = result
    return lista

@router.get("/{id}")
def get_by_id(id: str) -> Mensaje:
    return Mensaje.parse_obj(mensajes.find_one({"_id": ObjectId(id)}))

@router.post("/")
def post(mensaje: Mensaje):
    inserted_message: InsertOneResult = mensajes.insert_one(mensaje.dict(exclude_unset=True))
    created_message: Mensaje = Mensaje.parse_obj(mensajes.find_one({"_id": ObjectId(inserted_message.inserted_id)}))
    return created_message

@router.put("/{id}")
def put(id: str, mensaje: MensajePut):
    update_result : UpdateResult = mensajes.update_one({"_id": ObjectId(id)}, {"$set": mensaje.dict(exclude_unset=True)})
    if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Message with ID {id} not found")
    updated : Mensaje = Mensaje.parse_obj(mensajes.find_one({"_id": ObjectId(id)}))
    return updated

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str):
    delete_result: DeleteResult = mensajes.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count != 1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menssage with ID {id} not found")
    return f"Message with id {id} succesfully deleted"

@router.post("/{id}")
def post(id: str, mensaje: str, alias: str):
    contacto: UsuarioId = usuarios_api.get(alias=contacto.alias)[0]
    usuario: Usuario = usuarios_api.get_by_id(id)
    mensaje: Mensaje = Mensaje()
    inserted_message: InsertOneResult = mensajes.insert_one(mensaje.dict(exclude_unset=True))
    created_message: Mensaje = Mensaje.parse_obj(mensajes.find_one({"_id": ObjectId(inserted_message.inserted_id)}))
    return created_message
