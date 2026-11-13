# F1 Podium Predictor

Proyecto académico que estima si un piloto de Fórmula 1 terminará entre los tres primeros de una carrera. Incluye preparación de datos, entrenamiento, seguimiento de experimentos con MLflow, una API con FastAPI, una interfaz con Streamlit y un monitor de desempeño.

## Flujo del proyecto

Datos históricos de F1 → preparación de datos → entrenamiento y registro en MLflow → modelo serializado → API de predicción → interfaz web.

## Ejecución local

Desde la raíz del repositorio, con tu entorno virtual activo:

```bash
python -m pip install -r requirements.txt
python -m uvicorn src.api.main:app --reload
```

Con la API iniciada, abre [Swagger UI](http://127.0.0.1:8000/docs) para probar las predicciones. También puedes consultar `notebooks/03_Test_API.ipynb`.

## Monitoreo del desempeño

El script `model_monitor.py` lee `monitoring/current_model_metrics.json` y compara las métricas actuales con la línea base y los umbrales mínimos. Cuando una métrica cae por debajo de su umbral, imprime una alerta en la terminal y recomienda iniciar el runbook de degradación.

```bash
python model_monitor.py
```

### Resultados de la corrida de demostración

La clase positiva corresponde a **terminar en el podio**.

| Métrica | Qué mide | Línea base | Valor actual | Umbral mínimo | Estado |
|---|---|---:|---:|---:|---|
| Accuracy | Proporción total de predicciones correctas | 0.8799 | 0.8020 | 0.8400 | ALERTA |
| Precision | De los pilotos pronosticados para el podio, cuántos realmente llegaron | 0.5389 | 0.4100 | 0.4800 | ALERTA |
| Recall | De los pilotos que realmente llegaron al podio, cuántos identificó el modelo | 0.3765 | 0.2400 | 0.3300 | ALERTA |
| F1-score | Media armónica de precision y recall | 0.4433 | 0.3030 | 0.4000 | ALERTA |

El recall de `0.2400` indica que se identificó al 24 % de los pilotos que realmente llegaron al podio, según las métricas de esta corrida. Conviene revisar el F1 junto con precision y recall para entender cómo se desempeña el modelo en la clase que queremos predecir.

## Runbook de degradación del modelo

1. **Confirmar la alerta.** Guardar la salida del monitor con la fecha, los valores observados y los umbrales incumplidos.
2. **Diagnosticar.** Revisar qué versión del modelo y qué conjunto etiquetado generaron las métricas. Verificar que la evaluación sea comparable con la línea base.
3. **Intervenir.** Si se confirma un problema en los datos o en el preprocesamiento, corregirlo y volver a evaluar. Si el problema se atribuye a un cambio de modelo, evaluar la reversión a una versión estable.
4. **Verificar.** Ejecutar una nueva evaluación, actualizar el JSON con los resultados y correr el monitor. Si las métricas siguen bajo sus mínimos, mantener abierto el incidente.
5. **Documentar.** Guardar la alerta, la acción aplicada y la comparación antes y después.

Para demostrar el flujo en clase, se pueden inyectar valores de prueba en una copia del JSON. Esa corrida verifica el comportamiento del monitor y sus alertas. La recuperación del modelo se comprueba con una nueva evaluación sobre datos etiquetados.
