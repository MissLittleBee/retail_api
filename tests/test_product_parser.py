import os
import pytest
from lxml import etree
from app import ProductParser

@pytest.fixture
def test_data_xml():
    # Cesta k testovacímu XML souboru
    return os.path.join(os.path.dirname(__file__), 'test_data', 'test_data.xml')

@pytest.fixture
def parser(test_data_xml):
    # Vytvoření instance ProductParser pro testy
    return ProductParser(test_data_xml)

def test_product_count(parser):
    # Test pro získání počtu produktů
    assert parser.get_product_count() == 3, "Počet produktů by měl být 3."

def test_product_names(parser):
    # Test pro získání názvů produktů
    expected_names = [
        "Testovací produkt 1",
        "Testovací produkt 2",
        "Testovací produkt 3"
    ]
    assert parser.get_product_names() == expected_names, f"Názvy produktů se neshodují."

def test_spare_parts(parser):
    # Test pro získání náhradních dílů
    expected_spare_parts = {
        "product_spare_parts": [
            {
                "product": "Testovací produkt 1",
                "spare_part": [
                    {"code": "P1001", "name": "Testovací příslušenství 1"}
                ]
            },
            {
                "product": "Testovací produkt 2",
                "spare_part": [
                    {"code": "P1002", "name": "Testovací příslušenství 2"}
                ]
            },
            {
                "product": "Testovací produkt 3",
                "spare_part": [
                    {"code": "P1003", "name": "Testovací příslušenství 3"}
                ]
            }
        ]
    }
    assert parser.get_spare_parts() == expected_spare_parts, "Náhradní díly se neshodují."

