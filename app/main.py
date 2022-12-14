from fastapi import FastAPI
from .entities import usuarios, contactos, mensajes

# Create app
app = FastAPI()

# Import routers
app.include_router(
    usuarios.router,
    prefix="/usuarios",
    tags=["usuarios"]
)

app.include_router(
    contactos.router,
    prefix="/contactos",
    tags=["contactos"]
)

# Import routers
app.include_router(
    mensajes.router,
    prefix="/mensajes",
    tags=["mensajes"]
)

@app.get("/")
async def root():
    return {"message": "Welcome to Instant"}


