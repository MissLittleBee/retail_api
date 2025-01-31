import pytest
from app import ProductParser
import os

@pytest.fixture
def xml_file():
    """
    Fixture path for testing data.
    """
    return os.path.join(os.path.dirname(__file__), "test_data.xml")

def test_get_product_count(xml_file):
    parser = ProductParser(xml_file)
    assert parser.get_product_count() == 3

def test_get_product_names(xml_file):
    parser = ProductParser(xml_file)
    assert parser.get_product_names() == ["Product1", "Product2", "Product3"]

def test_get_spare_parts(xml_file):
    parser = ProductParser(xml_file)
    expected = [
        {"product": "Product1", "spare_part": "Part1"},
        {"product": "Product2", "spare_part": "Part2"}
    ]
    assert parser.get_spare_parts() == expected