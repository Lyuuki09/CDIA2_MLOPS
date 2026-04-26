import numpy as np
import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from typing import Tuple

# Exercício 1.2 e 1.3 func geradora com sabor de domínio (Garage Vintage)
def gerar_dataset_oficina(
    n_samples: int = 2000, 
    seed: int = 42, 
    proporcao_atraso: float = 0.3
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """Gera dados de projetos de restauração (Alvo: 1 para Atrasado, 0 para No Prazo)"""
    if not (0.05 <= proporcao_atraso <= 0.95):
        raise ValueError("A proporção deve estar entre 0.05 e 0.95")
    
    rng = np.random.default_rng(seed)
    atraso = rng.choice([0, 1], size=n_samples, p=[1-proporcao_atraso, proporcao_atraso])

    # Features baseadas no domínio Garage Vintage
    complexidade = np.where(atraso, rng.integers(7, 11, n_samples), rng.integers(1, 7, n_samples))
    disponibilidade_pecas = np.where(atraso, rng.choice([0, 1], n_samples, p=[0.8, 0.2]), rng.choice([0, 1], n_samples, p=[0.2, 0.8]))
    orcamento_inicial = rng.uniform(5000, 50000, n_samples).round(2)
    idade_veiculo = rng.integers(30, 80, n_samples)
    equipe_experiente = rng.choice([0, 1], n_samples)

    df = pd.DataFrame({
        "complexidade": complexidade,
        "disponibilidade_pecas": disponibilidade_pecas,
        "orcamento_inicial": orcamento_inicial,
        "idade_veiculo": idade_veiculo,
        "equipe_experiente": equipe_experiente,
        "target": atraso
    })

    X = df.drop(columns=["target"]).values
    y = df["target"].values
    return df, X, y

# Exercício 2.1 e 2.2 Treinamento e Serialização
print("--- Iniciando Treinamento ---")
df, X, y = gerar_dataset_oficina()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliação
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred, target_names=["No Prazo", "Atrasado"]))

# Salvando
joblib.dump(model, "model.pkl")
print(f"✅ Artefato salvo: model.pkl ({os.path.getsize('model.pkl')/1024:.1f} KB)")