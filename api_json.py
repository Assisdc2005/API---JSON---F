from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json
import os
import uvicorn

app = FastAPI()

JSON_PATH = r"C:\Users\matheus.assis\Downloads\fornecedores.json"

@app.get("/")
def raiz():
    return {"mensagem": "API funcionando! Use /fornecedores para acessar os dados."}

@app.get("/fornecedores")
def get_fornecedores():
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return JSONResponse(content=data)
    return JSONResponse(content={"erro": "Arquivo JSON não encontrado"}, status_code=404)

# Adicione esta parte
if __name__ == "__main__":
    uvicorn.run("api_json:app", host="127.0.0.1", port=8000, reload=True)