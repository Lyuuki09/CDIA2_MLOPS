from fastapi import FastAPI
from typing import Optional

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

@app.get("/cardapio")
async def listar_pratos(
    categoria: Optional[str] = None,
    preco_maximo: Optional[float] = None
):
    resultado = pratos

    if categoria:
        resultado = [p for p in resultado if p["categoria"] == categoria]

    if preco_maximo:
        resultado = [p for p in resultado if p["preco"] <= preco_maximo]

    return resultado

@app.get('/cardapio/{prato_id}')
async def buscar_prato(prato_id: int):
    for prato in pratos:
        if prato['id'] == prato_id:
            return prato
    return {'Mensagem': 'Prato não encontrado, qui qui qui qui!'}

@app.get("cardapio/{prato_id}/detalhes")
async def detalhes_prato(
    prato_id: int,
    incluir_ingredientes: bool = False,
    
):
    for prato in pratos:
        if prato['id'] == prato_id:
            if incluir_ingredientes:
                return {**prato, 'ingedientes':['...lista...']}
            return prato
    return {'mensagem': 'Prato não encontrado'}
        
