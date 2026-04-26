import os
import sklearn
import joblib as jl
from huggingface_hub import HfApi, login

# Substitua pelo seu token ou use variável de ambiente
HF_TOKEN = "SEU_TOKEN_AQUI" 
login(token=HF_TOKEN)

api = HfApi()
username = api.whoami()["name"]
repo_id = f"{username}/garage-vintage-atraso-v1"

# Criar Repositório Exercício 3.1
api.create_repo(repo_id=repo_id, repo_type="model", exist_ok=True)

# Criar Model Card Exercício 3.2
MODEL_CARD = f"""---
language: pt
tags:
  - sklearn
  - mlops
  - classic-cars
---
# Garage Vintage - Preditor de Atrasos
Modelo para prever se a restauração de um carro clássico atrasará.

## Features
- complexidade (1-10)
- disponibilidade_pecas (0 ou 1)
- orcamento_inicial (float)
- idade_veiculo (int)
- equipe_experiente (0 ou 1)
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(MODEL_CARD)

# Upload de arquivos [Exercício 3.3]
for file in ["model.pkl", "README.md"]:
    api.upload_file(
        path_or_fileobj=file,
        path_in_repo=file,
        repo_id=repo_id,
        commit_message=f"Add {file}"
    )
print(f" Modelo publicado em: https://huggingface.co/{repo_id}")