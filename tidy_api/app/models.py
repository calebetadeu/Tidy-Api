from sqlalchemy import Column, Integer, String, Float, JSON
from app.db.base_class import Base  # Certifique-se de importar o Base unificado
import json

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    codigo_tidy = Column(String, nullable=True)  # Campo já existente
    codigo_ditrator = Column(String, nullable=True)
    codigo_casa_dos_rolamentos = Column(String, nullable=True)
    codigo_romar_mann = Column(String, nullable=True)
    nome_fantasia = Column(String, nullable=True)
    razao_social = Column(String, nullable=True)
    rota = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    estado = Column(String, nullable=True)
    empresas_trabalhadas = Column(JSON, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    cnpj = Column(String, nullable=True)  # Novo campo adicionado

    def get_empresas(self):
        if not self.empresas_trabalhadas:
            return []
        try:
            return json.loads(self.empresas_trabalhadas)
        except json.JSONDecodeError:
            return []

    def set_empresas(self, value):
        self.empresas_trabalhadas = json.dumps(value) if value else "[]"