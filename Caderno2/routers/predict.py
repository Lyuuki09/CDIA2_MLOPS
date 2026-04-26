from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import numpy as np
from model_utils import load_model

router = APIRouter()
REPO_ID = "SEU_USUARIO/garage-vintage-atraso-v1" # Atualize aqui
_model = None

def get_model():
    global _model
    if _model is None:
        _model = load_model(REPO_ID)
    return _model

class PredictInput(BaseModel):
    complexidade: int = Field(ge=1, le=10)
    disponibilidade_pecas: int = Field(ge=0, le=1)
    orcamento_inicial: float = Field(gt=0)
    idade_veiculo: int = Field(ge=20)
    equipe_experiente: int = Field(ge=0, le=1)

@router.post("/predict")
async def predict(data: PredictInput):
    model = get_model()
    features = np.array([[
        data.complexidade, data.disponibilidade_pecas, 
        data.orcamento_inicial, data.idade_veiculo, data.equipe_experiente
    ]])
    
    prediction = int(model.predict(features)[0])
    prob = float(model.predict_proba(features)[0][1])
    
    return {
        "atraso": bool(prediction),
        "probabilidade_atraso": round(prob, 4),
        "status": "Atrasado" if prediction == 1 else "No Prazo"
    }

@router.get("/health")
async def health():
    try:
        model = get_model()
        model.predict(np.zeros((1, 5)))
        return {"status": "ok", "model": "loaded"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "degraded", "error": str(e)})