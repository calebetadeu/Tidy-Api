# app/endpoints/pdf.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from io import BytesIO
import re
from PyPDF2 import PdfReader
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class MatchData(BaseModel):
    Prefixo: str
    No_Titulo: str
    Parcela: Optional[str] = ""
    Cliente: str
    Nome: str
    Dt_Comissao: str
    Vencto: str
    Origem: str
    Dt_Baixa: str
    Data_Pagto: str
    Pedido: str
    Vlr_Titulo: str
    Vlr_Base: str
    Percentual: str
    Comissao_Tipo: str
    Ajuste: str
    Vendedor: str

class ExtractResponse(BaseModel):
    data: List[MatchData]

def extrair_texto_pdf_bytes(file_bytes: bytes):
    reader = PdfReader(BytesIO(file_bytes))
    textos = []
    for pagina in reader.pages:
        texto = pagina.extract_text()
        if texto:
            textos.append(texto)
    return textos

def processar_linhas(textos: List[str]):
    dados = []
    # Expressão regular para capturar os campos conforme o padrão
    pattern = re.compile(
        r"^(?P<Prefixo>\d{1,3})\s+"
        r"(?P<No_Titulo>\d+)\s+"
        r"(?:(?P<Parcela>\d{2})\s+)?"
        r"(?P<Cliente>\S+)\s+"
        r"(?P<Nome>.+?)\s+"
        r"(?P<Dt_Comissao>\d{2}/\d{2}/\d{4}|/ /)\s+"
        r"(?P<Vencto>\d{2}/\d{2}/\d{4}|/ /)\s+"
        r"(?P<Origem>\S*)\s+"
        r"(?P<Dt_Baixa>\d{2}/\d{2}/\d{4}|/ /)\s+"
        r"(?P<Data_Pagto>/ /)\s+"
        r"(?P<Pedido>\S*)\s*"
        r"(?P<Vlr_Titulo>-?\d+\.\d{3},\d{2})\s+"
        r"(?P<Vlr_Base>-?\d+\.\d{3},\d{2})\s+"
        r"(?P<Percentual>\d+,\d{2})\s+"
        r"(?P<Comissao_Tipo>-?\d+,\d{2}\s+[A-Z])\s*"
        r"(?P<Ajuste>\S*)\s*"
        r"(?P<Vendedor>\d{6})$"
    )
    for texto in textos:
        linhas = texto.split('\n')
        for linha in linhas:
            linha = linha.strip()
            # Ignorar cabeçalhos ou linhas irrelevantes
            if any(header in linha for header in [
                'Prefixo', 'No. Titulo', 'Parcela', 'Cliente',
                'Nome', 'Dt Comissao', 'Vencto', 'Vlr Base'
            ]):
                continue
            match = pattern.match(linha)
            if match:
                match_data = match.groupdict()
                if match_data.get('Parcela') is None:
                    match_data['Parcela'] = ''
                # Ajuste: verifica se o campo 'Nome' possui a data de comissão grudada
                nome = match_data['Nome']
                dt_comissao = match_data['Dt_Comissao']
                nome_e_data = nome + dt_comissao
                nome_match = re.match(r'(.+?)(\d{2}/\d{2}/\d{4}|/ /)$', nome_e_data)
                if nome_match:
                    match_data['Nome'] = nome_match.group(1).strip()
                    match_data['Dt_Comissao'] = nome_match.group(2)
                else:
                    nome_match = re.match(r'(.+?)(\d{2}/\d{2}/\d{4}|/ /)$', nome)
                    if nome_match:
                        match_data['Nome'] = nome_match.group(1).strip()
                        match_data['Dt_Comissao'] = nome_match.group(2)
                dados.append(match_data)
            else:
                # Fallback: separar os dados usando split, caso a regex não bata
                partes = linha.split()
                if len(partes) >= 16:
                    if len(partes[2]) == 2:
                        parcela = partes[2]
                        cliente_idx = 3
                    else:
                        parcela = ''
                        cliente_idx = 2
                    match_data = {
                        'Prefixo': partes[0],
                        'No_Titulo': partes[1],
                        'Parcela': parcela,
                        'Cliente': partes[cliente_idx],
                        'Nome': ' '.join(partes[cliente_idx + 1:-12]),
                        'Dt_Comissao': partes[-12],
                        'Vencto': partes[-11],
                        'Origem': partes[-10],
                        'Dt_Baixa': partes[-9],
                        'Data_Pagto': partes[-8],
                        'Pedido': partes[-7],
                        'Vlr_Titulo': partes[-6],
                        'Vlr_Base': partes[-5],
                        'Percentual': partes[-4],
                        'Comissao_Tipo': partes[-3] + ' ' + partes[-2],
                        'Ajuste': '',
                        'Vendedor': partes[-1],
                    }
                    # Ajusta o campo 'Nome' se a data de comissão estiver grudada
                    nome = match_data['Nome']
                    dt_comissao = match_data['Dt_Comissao']
                    nome_e_data = nome + dt_comissao
                    nome_match = re.match(r'(.+?)(\d{2}/\d{2}/\d{4}|/ /)$', nome_e_data)
                    if nome_match:
                        match_data['Nome'] = nome_match.group(1).strip()
                        match_data['Dt_Comissao'] = nome_match.group(2)
                    else:
                        nome_match = re.match(r'(.+?)(\d{2}/\d{2}/\d{4}|/ /)$', nome)
                        if nome_match:
                            match_data['Nome'] = nome_match.group(1).strip()
                            match_data['Dt_Comissao'] = nome_match.group(2)
                    dados.append(match_data)
                else:
                    continue
    return dados

@router.post("/extract", response_model=ExtractResponse)
async def extract_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="O arquivo enviado deve ser um PDF.")
    try:
        file_bytes = await file.read()
        textos = extrair_texto_pdf_bytes(file_bytes)
        dados = processar_linhas(textos)
        return {"data": dados}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))