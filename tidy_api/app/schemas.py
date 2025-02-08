from typing import List, Optional
from pydantic import BaseModel

class ClientBase(BaseModel):
    codigo_tidy: Optional[str] = None
    cnpj: Optional[str] = None  # Novo campo adicionado
    codigo_ditrator: Optional[str] = None
    codigo_casa_dos_rolamentos: Optional[str] = None
    codigo_romar_mann: Optional[str] = None
    nome_fantasia: Optional[str] = None
    razao_social: Optional[str] = None
    rota: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    empresas_trabalhadas: Optional[List[str]] = []
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True

class StateLocations(BaseModel):
    estado: str
    cidades: List[str]

    class Config:
        orm_mode = True