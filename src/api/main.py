import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# Crear app
app = FastAPI(
    title="F1 Podium Predictor API",
    description="API para predecir si un piloto de Fórmula 1 terminará en el podio.",
    version="1.0.0"
)

# Cargar modelo
model = joblib.load("models/f1_podium_model.pkl")


class PredictionInput(BaseModel):
    driver: str
    constructor: str
    circuit: str
    year: int
    grid: int


@app.get("/")
def home():
    return {
        "message": "F1 Podium Predictor API is running"
    }


@app.post("/predict")
def predict(data: PredictionInput):
    input_df = pd.DataFrame([data.model_dump()])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    return {
        "podium_prediction": int(prediction),
        "podium_probability": round(float(probability), 4)
    }