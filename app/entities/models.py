from pydantic import BaseModel, Field
from datetime import datetime
from bson.objectid import ObjectId
from pydantic.json import ENCODERS_BY_TYPE

ENCODERS_BY_TYPE[ObjectId]=str

# Models
class Mensaje(BaseModel):
    timestamp : datetime
    origen : int
    destino : int
    texto : str

class Contacto(BaseModel):
    telefono : int 
    alias : str 

class Usuario(Contacto):
    contactos : list[Contacto] | None

# For Id 

class UsuarioId(Usuario):
    id : str = Field(alias="_id")

# For PUT
class MensajePut(BaseModel):
    timestamp : datetime | None
    origen : int | None
    destino : int | None
    texto : str | None