from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import json
import os
import re
import uvicorn

app = FastAPI()

JSON_PATH = r"C:\Users\matheus.assis\Downloads\JSON\fornecedores.json"

def limpar_cnpj(cnpj: str) -> str:
    return re.sub(r"\D", "", cnpj)
#carregar dados
def carregar_fornecedores():
    if not os.path.exists(JSON_PATH):
        raise HTTPException(status_code=404, detail="Arquivo JSON não encontrado")
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

@app.get("/")
def raiz():
    return {"mensagem": "API funcionando! Use /fornecedores para acessar os dados."}

# Retorna todos os fornecedores
@app.get("/fornecedores")
def get_fornecedores():
    return carregar_fornecedores()

# Busca fornecedor por CNPJ exato
@app.get("/fornecedores/{cnpj}")
def get_fornecedor_por_cnpj(cnpj: str):
    fornecedores = carregar_fornecedores()
    cnpj_limpo = limpar_cnpj(cnpj)

    for fornecedor in fornecedores:
        if limpar_cnpj(fornecedor.get("CNPJ", "")) == cnpj_limpo:
            return fornecedor

    raise HTTPException(status_code=404, detail=f"Fornecedor com CNPJ {cnpj} não encontrado")

# Filtro por CNPJ, Nome, Email e Conectado
@app.get("/fornecedores/filtro")
def filtrar_fornecedores(
    cnpj: str = Query(None),
    nome: str = Query(None),
    email: str = Query(None),
    conectado: str = Query(None)  # Espera "Sim" ou "Não"
):
    fornecedores = carregar_fornecedores()
    resultados = fornecedores

    if cnpj:
        cnpj_limpo = limpar_cnpj(cnpj)
        resultados = [f for f in resultados if limpar_cnpj(f.get("CNPJ", "")) == cnpj_limpo]

    if nome:
        resultados = [f for f in resultados if nome.lower() in f.get("Nome", "").lower()]

    if email:
        resultados = [f for f in resultados if email.lower() in f.get("Email", "").lower()]

    if conectado:
        resultados = [f for f in resultados if f.get("Conectado", "").lower() == conectado.lower()]

    if not resultados:
        return JSONResponse(content={"mensagem": "Nenhum fornecedor encontrado"}, status_code=404)

    return resultados

if __name__ == "__main__":
    uvicorn.run("api_json:app", host="127.0.0.1", port=8000, reload=True)
