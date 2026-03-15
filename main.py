# main.py
from fastapi import FastAPI
from infrastructure.api.routes import usuarios

app = FastAPI(
    title="Arándanos ERP API",
    description="Backend para gestión de cultivo y ventas de arándanos",
    version="1.0.0"
)

# Incluir las rutas
app.include_router(usuarios.router)

@app.get("/")
def root():
    return {"mensaje": "Bienvenido a la API del sistema de Arándanos"}