# create_db.py
from tidy_api.app.database import engine, Base
from tidy_api.app.models import *  # Importa todos os seus modelos

def criar_banco():
    Base.metadata.create_all(bind=engine)
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    criar_banco()