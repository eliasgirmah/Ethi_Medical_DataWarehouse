from fastapi.testclient import TestClient
from app.main import app  # Assuming `app` is your FastAPI instance

client = TestClient(app)

def test_database_connection():
    response = client.get("/transform_data")
    assert response.status_code == 200
    assert response.json() == {"status": "connected"}
