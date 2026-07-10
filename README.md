# F1 Podium Predictor

Proyecto académico para entrenar, registrar, desplegar y consumir un modelo de IA que predice si un piloto de Fórmula 1 terminará en el podio.

## Arquitectura

Dataset F1 → Entrenamiento → MLflow → Modelo .pkl → FastAPI → Streamlit → Cloud

## Tecnologías

- Python
- Pandas
- Scikit-learn
- MLflow
- FastAPI
- Streamlit
- Joblib

## Ejecución local

### API

```bash
uvicorn src.api.main:app --reload