# import_routes.py
import csv
from app.database import SessionLocal, engine, Base
from app.models import Client

# Se ainda não criou as tabelas, este comando as cria:
Base.metadata.create_all(bind=engine)

def converter_coordenada(valor: str) -> float:
    """
    Converte o valor de coordenada do formato do CSV para float.
    Por exemplo, se o CSV contém "-270.922.364", 
    assumindo que os dois primeiros dígitos representam a parte inteira,
    o resultado será -27.0922364.
    """
    if not valor:
        return None
    # Remove todos os pontos
    numero = valor.replace('.', '')
    sinal = -1 if numero.startswith('-') else 1
    if numero.startswith('-'):
        numero = numero[1:]
    # Aqui, assumimos que para as coordenadas brasileiras (latitude e longitude)
    # os dois primeiros dígitos correspondem à parte inteira.
    if len(numero) < 3:
        return None
    parte_inteira = numero[:2]
    parte_decimal = numero[2:]
    try:
        return float(f"{'-' if sinal < 0 else ''}{parte_inteira}.{parte_decimal}")
    except ValueError:
        return None

def importar_rotas(csv_path: str):
    db = SessionLocal()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cidade = row.get("Cidade")
            estado = row.get("Estado")
            rota = row.get("Rota")
            lat_str = row.get("Latitude")
            long_str = row.get("Longitude")
            
            # Converter as coordenadas
            latitude = converter_coordenada(lat_str) if lat_str else None
            longitude = converter_coordenada(long_str) if long_str else None

            # Busque os clientes que correspondem à combinação de Cidade, Estado e Rota
            clientes = db.query(Client).filter(
                Client.cidade == cidade,
                Client.estado == estado,
                Client.rota == rota
            ).all()
            
            if not clientes:
                print(f"Nenhum cliente encontrado para {cidade} - {estado} - {rota}")
            for cliente in clientes:
                cliente.latitude = latitude
                cliente.longitude = longitude
                print(f"Atualizando cliente {cliente.id}: {cidade} - {rota} com lat={latitude} e long={longitude}")
            db.commit()
    db.close()
    print("Importação de rotas concluída.")

if __name__ == "__main__":
    # Substitua "rotas.csv" pelo caminho correto do seu arquivo CSV de rotas.
    importar_rotas("rotas.csv")