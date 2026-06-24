import pytest
from fastapi.testclient import TestClient
import numpy as np
from api.app import app, models

class DummyModel:
    def predict(self, df):
        return np.array([15000.0])

@pytest.fixture(autouse=True)
def setup_model():
    models["insurance_model"] = DummyModel()

client = TestClient(app)

def test_predict_ok():
    payload = {
        "age": 25,
        "sex": "female",
        "bmi": 24.3,
        "children": 1,
        "smoker": "no",
        "region": "northwest"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json() == {"predictions": [15000.0]}

def test_predict_validation_error():
    payload = {
        "age": 25,
        "sex": "female"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
