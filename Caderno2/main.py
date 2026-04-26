from fastapi import FastAPI
from routers import predict # Certifique-se de que a pasta routers tenha o __init__.py

app = FastAPI(title="Garage Vintage API")

# Incluindo a nova rota de ML
app.include_router(predict.router, prefix="/ml", tags=["Machine Learning"])

@app.get("/")
async def root():
    return {"message": "Garage Vintage API Online"}