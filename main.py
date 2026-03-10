from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI(
    title="Bella Tavola API",
    description="API do restaurante Bella Tavola",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "restaurante": "Bella Tavola",
        "mensagem": "Bem-vindo à nossa API",
        "chefe": "Rei Ratao",
        "cidade": "Olinda",
        "especialidade": "Rato"
    }

pratos = [
    {'id': 1, 'nome': 'rato assado', 'categoria': 'carne', 'preco': 60.0, "disponivel": False},
    {'id': 2, 'nome': 'rato cozido', 'categoria': 'carne', 'preco': 50.0, "disponivel": False},
    {'id': 3, 'nome': 'pitú', 'categoria': 'bebidas', 'preco': 2.5, "disponivel": True},
    {'id': 4, 'nome': 'batata frita', 'categoria': 'porcao', 'preco': 20.0, "disponivel": True},
    {'id': 5, 'nome': 'batata crua', 'categoria': 'porcao', 'preco': 200.0, "disponivel": True},
    {'id': 6, 'nome': 'rato cru', 'categoria': 'carnes', 'preco': 20, "disponivel": False},
    {'id': 7, 'nome': 'vinho carreteiro', 'categoria': 'bebidas', 'preco': 10.0, "disponivel": True}
]

class Inserir_Prato(BaseModel):
    nome: str
    categoria: str
    preco: float
    disponivel: bool = True

@app.post('/pratos')
async def criar_prato(prato: PratoInput):
    novo_id = max(p['id'] for p in pratos) + 1
    novo_prato = {'id': novo_id, **pratos.model_dump()}
    pratos.append(novo_prato)


@app.get("/cardapio")
async def olhar_cardapio(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None,
    apenas_disponivel: bool = False
):
    resultado = pratos

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]
    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]
    if apenas_disponivel:
        resultado = [p for p in resultado if p['disponivel']] 
    return resultado

@app.get("/cardapio/{prato_id}")
async def detalhar_prato(prato_id: int, formato: str = 'completo'):
    for prato in pratos:
        if prato['id'] == prato_id :
            if formato == "resumido":
                return {"nome": prato['nome'], 'preço': prato['preco']}
            return prato
    return {'mensagem': 'Prato não encontrado'}







# @app.get('/cardapio/{prato_id}')
# async def buscar_prato(prato_id: int):
#     for prato in pratos:
#         if prato['id'] == prato_id:
#             return prato
#     return {'Mensagem': 'Prato não encontrado, qui qui qui qui!'}


