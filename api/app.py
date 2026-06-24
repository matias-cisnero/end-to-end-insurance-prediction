from contextlib import asynccontextmanager
from fastapi import FastAPI
import mlflow
import pandas as pd
from pydantic import BaseModel

from config import MODEL_URI, MLFLOW_TRACKING_URI

models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    model = mlflow.pyfunc.load_model(MODEL_URI)
    models["insurance_model"] = model
    yield

    models.clear()

app = FastAPI(lifespan=lifespan)

class InputData(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str

@app.post("/predict")
def predict(data: InputData):
    data_df = pd.DataFrame([data.model_dump()])

    model = models["insurance_model"]
    predictions = model.predict(data_df)

    return {"predictions": predictions.tolist()}
