from fastapi import FastAPI
from src.core.database import engine, Base
from src.features.auth.domain import models

# Crear las tablas en PostgreSQL si no existen
# (En producción, usar Alembic para migraciones)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Arándanos Fam", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API del Cultivo de Arándanos"}