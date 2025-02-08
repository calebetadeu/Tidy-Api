# app/main.py
from unittest.mock import Base
from django.template import engines
from fastapi import FastAPI
from app.endpoints import clients, pdf
from app.database import engine, Base
from app.models import *  # Importa todos os seus modelos

app = FastAPI()
Base.metadata.create_all(bind=engine)
# Inclui os endpoints com o prefixo /api
app.include_router(clients.router, prefix="/api")
app.include_router(pdf.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à API do projeto!"}