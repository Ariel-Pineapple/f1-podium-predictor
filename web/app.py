import streamlit as st
import requests

st.set_page_config(page_title="F1 Podium Predictor", page_icon="🏎️")

st.title("🏎️ F1 Podium Predictor")
st.write("Predice si un piloto de Fórmula 1 terminará en el podio.")

driver = st.text_input("Piloto", "Hamilton")
constructor = st.text_input("Constructor", "McLaren")
circuit = st.text_input("Circuito", "albert_park")
year = st.number_input("Año", min_value=1950, max_value=2025, value=2008)
grid = st.number_input("Posición de salida", min_value=1, max_value=30, value=1)

if st.button("Predecir podio"):
    data = {
        "driver": driver,
        "constructor": constructor,
        "circuit": circuit,
        "year": int(year),
        "grid": int(grid)
    }

    response = requests.post(
        "http://127.0.0.1:8000/predict",
        json=data
    )

    result = response.json()

    probability = result["podium_probability"]
    prediction = result["podium_prediction"]

    st.subheader("Resultado")

    if prediction == 1:
        st.success(f"🏆 Alta probabilidad de podio: {probability * 100:.2f}%")
    else:
        st.warning(f"Sin podio probable: {probability * 100:.2f}%")