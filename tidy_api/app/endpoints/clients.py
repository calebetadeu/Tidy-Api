from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import crud, schemas, models
from app.database import SessionLocal, engine

router = APIRouter()

# Cria as tabelas no banco de dados, se ainda não existirem
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/clients/filter", response_model=List[schemas.Client])
def filter_clients(
    razao_social: Optional[str] = None,
    estado: Optional[str] = None,
    cidade: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Client)
    
    if razao_social:
        query = query.filter(models.Client.razao_social.ilike(f"%{razao_social}%"))
    
    if estado:
        # Usa o atributo 'estado' que existe no modelo
        query = query.filter(func.lower(models.Client.estado) == estado.lower())
    
    if cidade:
        # Usa o atributo 'cidade' para filtrar
        query = query.filter(func.lower(models.Client.cidade) == cidade.lower())
    
    clients = query.all()
    if not clients:
        raise HTTPException(status_code=404, detail="Nenhum cliente encontrado com os filtros informados")
    return clients

@router.get("/clients/locations", response_model=List[schemas.StateLocations])
def get_client_locations(db: Session = Depends(get_db)):
    # Usa o campo 'estado' em vez de 'codigo'
    estados_tuples = db.query(models.Client.estado).distinct().all()
    if not estados_tuples:
        raise HTTPException(status_code=404, detail="Nenhum estado encontrado")
    
    state_locations = []
    for (estado,) in estados_tuples:
        # Usa o campo 'cidade' para obter as cidades correspondentes ao estado
        cidades_tuples = (
            db.query(models.Client.cidade)
            .filter(func.lower(models.Client.estado) == estado.lower())
            .distinct()
            .all()
        )
        cidades = [cidade for (cidade,) in cidades_tuples if cidade]
        state_locations.append(schemas.StateLocations(estado=estado, cidades=cidades))
    return state_locations

@router.get("/clients/", response_model=List[schemas.Client])
def read_clients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_clients(db, skip=skip, limit=limit)

@router.get("/clients/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Se a lista de empresas estiver errada, converte de JSON para lista
    if isinstance(db_client.empresas_trabalhadas, str):
        import json
        db_client.empresas_trabalhadas = json.loads(db_client.empresas_trabalhadas)

    return db_client
@router.post("/clients/", response_model=schemas.Client, status_code=status.HTTP_201_CREATED)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, client)

@router.put("/clients/{client_id}", response_model=schemas.Client)
def update_client(client_id: int, client: schemas.ClientCreate, db: Session = Depends(get_db)):
    db_client = crud.update_client(db, client_id, client)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@router.delete("/clients/{client_id}", response_model=schemas.Client)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.delete_client(db, client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client