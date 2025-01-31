import pytest
import os
from app import create_app

@pytest.fixture
def xml_file():
    """
    Fixture pro cestu k testovacímu XML souboru.
    """
    return os.path.join(os.path.dirname(__file__), "test_data.xml")

@pytest.fixture
def app(xml_file):
    """
    Fixture for creating Flask app.
    """
    app = create_app(xml_file)
    return app

@pytest.fixture
def client(app):
    """
    Fixture for testing client.
    """
    return app.test_client()

def test_index(client):
    """
    Testing endpoint `/` (Index).
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data

def test_count_products(client):
    """
    Testing endpoint `/count`.
    """
    response = client.get("/count")
    assert response.status_code == 200
    assert response.json == {"product_count": 3}

def test_names(client):
    """
    Testing endpoint `/names`.
    """
    response = client.get("/names")
    assert response.status_code == 200
    assert response.json == {"product_names": ["Product1", "Product2", "Product3"]}

def test_spare_parts(client):
    """
    Testing endpoint `/spare_parts`.
    """
    response = client.get("/spare_parts")
    assert response.status_code == 200
    assert response.json == {
        "product_spare_parts": [
            {"product": "Product1", "spare_part": "Part1"},
            {"product": "Product2", "spare_part": "Part2"}
        ]
    }