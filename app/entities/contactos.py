from fastapi import APIRouter, status, HTTPException, Depends
from pymongo.collection import Collection
from pydantic import Field
from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from pydantic.json import ENCODERS_BY_TYPE
from pymongo.results import UpdateResult, DeleteResult

from ..database import db
from .models import *
from . import usuarios as usuarios_api

ENCODERS_BY_TYPE[ObjectId]=str

# Create app
router = APIRouter()

# Collection
usuarios : Collection = db.usuarios

# API

@router.get("/{id}")
def get(id: str, match: str | None = None):
    lista: list[Contacto] = list(usuarios_api.get_by_id(id).contactos)

    if match is not None:
        result: list[Contacto] = []
        for contacto in lista:
            contacto: Contacto = Contacto.parse_obj(contacto)
            if match in contacto.alias:
                result.append(contacto)
        lista = result
    return lista

@router.post("/{id}")
def post(id: str, contactos: list[Contacto]):
    usuario: Usuario = usuarios_api.get_by_id(id)
    usuario.contactos = contactos
    return usuarios_api.put(id, usuario).contactos
"""
    for contacto in contactos:
        contacto: UsuarioId = usuarios_api.get(alias=contacto.alias)[0]
        put(contacto.id, usuario)
"""

@router.put("/{id}")
def put(id: str, contacto: Contacto):
    usuario: Usuario = usuarios_api.get_by_id(id)
    if usuario.contactos is None:
        usuario.contactos = [contacto]
    else:
        usuario.contactos.append(contacto)
    return usuarios_api.put(id, usuario).contactos

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: str):
    usuario: Usuario = usuarios_api.get_by_id(id)
    usuario.contactos = None
    return usuarios_api.put(id, usuario)
