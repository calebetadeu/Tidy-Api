import csv
import os
from tidy_api.app.database import SessionLocal, engine, Base
from tidy_api.app.models import Client

def recreate_database():
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Banco recriado.")

def csv_para_json(csv_path: str):
    data = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        # Limpa os nomes dos campos removendo espaços extras
        if reader.fieldnames:
            reader.fieldnames = [field.strip() for field in reader.fieldnames]
        for row in reader:
            data.append(row)
    return data

def importar_clientes(csv_path: str):
    if not os.path.exists(csv_path):
        print(f"Arquivo '{csv_path}' não encontrado!")
        return

    db = SessionLocal()
    data = csv_para_json(csv_path)
    
    # (Opcional) Debug: Verifica as chaves e o valor do campo "Codigo Tidy" na primeira linha
    if data:
        print("Chaves da primeira linha:", list(data[0].keys()))
        print("Valor de 'Codigo Tidy':", data[0].get("Codigo Tidy", "").strip())
    
    for row in data:
        codigo_ditrator = row.get("Codigo Ditrator", "").strip()
        codigo_tidy = row.get("Codigo Tidy", "").strip()
        codigo_casa_dos_rolamentos = row.get("Codigo Casa Dos Rolamentos", "").strip()
        codigo_romar_mann = row.get("Codigo Romar Mann", "").strip()
        nome_fantasia = row.get("Nome Fantasia", "").strip()
        razao_social = row.get("Razão Social", "").strip()
        rota = row.get("Rota", "").strip()
        cidade = row.get("Cidade", "").strip()
        estado = row.get("Estado", "").strip()
        cnpj = row.get("CNPJ", "").strip()
        # Processamento do campo "Empresas Trabalhadas"
        empresas_str = row.get("Empresas Trabalhadas", "").strip()
        empresas_list = [empresa.strip() for empresa in empresas_str.split(" - ")] if empresas_str else []

        # Logs para debug
        print(f"Empresas Trabalhadas (raw): '{empresas_str}'")
        print(f"Empresas Trabalhadas (list): {empresas_list}")

        # Log para verificar o valor de codigo_tidy
        print(f"Valor de 'Codigo Tidy': '{codigo_tidy}'")

        try:
            latitude = float(row.get("Latitude", "0") or 0)
        except ValueError:
            latitude = 0.0
        try:
            longitude = float(row.get("Longitude", "0") or 0)
        except ValueError:
            longitude = 0.0

        cliente = Client(
            codigo_ditrator=codigo_ditrator,
            codigo_casa_dos_rolamentos=codigo_casa_dos_rolamentos,
            codigo_romar_mann=codigo_romar_mann,
            codigo_tidy=codigo_tidy,
            cnpj=cnpj,
            nome_fantasia=nome_fantasia,
            razao_social=razao_social,
            rota=rota,
            cidade=cidade,
            estado=estado,
            empresas_trabalhadas=empresas_list,
            latitude=latitude,
            longitude=longitude
        )

        print("Importando cliente:", cliente)
        db.add(cliente)

    db.commit()
    db.close()
    print("Importação concluída.")

if __name__ == "__main__":
    recreate_database()
    importar_clientes("banco_clients_tidy.csv")