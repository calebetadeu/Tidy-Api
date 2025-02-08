# create_db.py
from app.database import engine, Base
from app.models import *  # Importa todos os seus modelos

def criar_banco():
    Base.metadata.create_all(bind=engine)
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_banco()