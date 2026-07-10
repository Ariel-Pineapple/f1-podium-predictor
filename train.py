import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# 1. Cargar dataset

print("Iniciando entrenamiento del modelo de Fórmula 1 para predecir si un piloto terminará en el podio...")
df = pd.read_csv("data/processed/f1_dataset.csv")  # ajusta si tu archivo se llama diferente

print("Dataset cargado:")
print(df.head())

# 2. Separar variables
X = df.drop(columns=["podium"])
y = df["podium"]

# 3. Convertir columnas de texto a columnas numéricas
X = pd.get_dummies(X, columns=["driver", "constructor", "circuit"], drop_first=True)

print("Columnas después de One-Hot Encoding:")
print(X.dtypes)
print(X.head())

# 4. Dividir datos
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 5. Entrenar modelo
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# 6. Evaluar
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print(f"Accuracy:  {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")

# 7. Guardar modelo
os.makedirs("models", exist_ok=True)

with open("models/f1_podium_model.pkl", "wb") as f:
    pickle.dump(model, f)

# 8. Guardar columnas usadas
with open("models/model_columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("Modelo guardado en models/f1_podium_model.pkl")
print("Columnas guardadas en models/model_columns.pkl")