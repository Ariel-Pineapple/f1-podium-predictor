from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

# 1. Inicializar la app
app = FastAPI(title="API de Predicción de Fraude - E-commerce")

# 2. Definir la estructura estricta de los datos de entrada
class TransactionInput(BaseModel):
    amount: float
    user_age: int
    device_type: int  # Asumiendo codificación numérica (ej. 0: mobile, 1: desktop)

# 3. Cargar el modelo al inicializar
MODEL_PATH = os.path.join(os.path.dirname(__file__), "modelo.pkl")
model = joblib.load(MODEL_PATH)

@app.get("/")
def read_root():
    return {"status": "API Ejecutándose correctamente"}

@app.post("/predict")
def predict_fraude(data: TransactionInput):
    # Convertir el payload JSON recibido a la estructura que espera el modelo
    input_data = [[data.amount, data.user_age, data.device_type]]
    
    # Realizar la predicción
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1] # Probabilidad de la clase 1 (Fraude)
    
    return {
        "is_fraud": bool(prediction),
        "fraud_probability": float(probability)
    }