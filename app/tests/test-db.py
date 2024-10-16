import sys
import os
from fastapi.testclient import TestClient

# Ensure the `app` module can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Import the FastAPI app instance
from app.main import app

client = TestClient(app)

def test_database_connection():
    response = client.get("/transform_data")
    assert response.status_code == 200
    assert response.json() == {"status": "connected"}  # Adjust this according to your actual API response
