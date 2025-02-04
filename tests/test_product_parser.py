import os
import unittest
from app import ProductParser


class TestProductParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # making up xml test file with czech names of products
        cls.test_xml_path = "data/test_products.xml"
        cls.test_data = """<?xml version="1.0" encoding="UTF-8"?>
<products>
    <item code="T1001" name="Testovací produkt 1" brand="TestBrand" czk="999.00" eur="39.99" stock="true">
        <descriptions>
            <description title="Charakteristika">Toto je testovací produkt 1.</description>
        </descriptions>
        <specs>
            <spec name="Hmotnost">500 g</spec>
            <spec name="Rozměr">100 x 50 x 30 mm</spec>
        </specs>
        <parts>
            <part name="Doporučené příslušenství">
                <item code="P1001" name="Testovací příslušenství 1" />
            </part>
        </parts>
    </item>
    <item code="T1002" name="Testovací produkt 2" brand="TestBrand" czk="1299.00" eur="49.99" stock="false">
        <descriptions>
            <description title="Charakteristika">Toto je testovací produkt 2.</description>
        </descriptions>
        <specs>
            <spec name="Hmotnost">750 g</spec>
            <spec name="Rozměr">120 x 60 x 40 mm</spec>
        </specs>
        <parts>
            <part name="Doporučené příslušenství">
                <item code="P1002" name="Testovací příslušenství 2" />
            </part>
        </parts>
    </item>
    <item code="T1003" name="Testovací produkt 3" brand="TestBrand" czk="1899.00" eur="79.99" stock="true">
        <descriptions>
            <description title="Charakteristika">Toto je testovací produkt 3.</description>
        </descriptions>
        <specs>
            <spec name="Hmotnost">1.2 kg</spec>
            <spec name="Rozměr">200 x 100 x 50 mm</spec>
        </specs>
        <parts>
            <part name="Doporučené příslušenství">
                <item code="P1003" name="Testovací příslušenství 3" />
            </part>
        </parts>
    </item>
</products>"""

        # saving test file
        os.makedirs("data", exist_ok=True)
        with open(cls.test_xml_path, "w", encoding="utf-8") as f:
            f.write(cls.test_data)

    @classmethod
    def tearDownClass(cls):
        # deleting test file after complete testing
        os.remove(cls.test_xml_path)
        os.rmdir("data")

    def setUp(self):
        # Initialization of object ProductParser
        self.parser = ProductParser(self.test_xml_path)

    def test_get_product_count(self):
        # Counting test
        self.assertEqual(self.parser.get_product_count(), 6)

    def test_get_product_names(self):
        # Testing result of extracting names
        expected_names = ['Testovací produkt 1',
                          'Testovací produkt 2',
                          'Testovací produkt 3',
                          'Testovací příslušenství 1',
                          'Testovací příslušenství 2',
                          'Testovací příslušenství 3']
        self.assertEqual(sorted(self.parser.get_product_names()), sorted(expected_names))

    def test_get_spare_parts(self):
        # Testing extracting product name and hist spare parts
        expected_spare_parts = {
            "product_spare_parts": [
                {
                    "product": "Testovací produkt 1",
                    "spare_part": [{"code": "P1001", "name": "Testovací příslušenství 1"}]
                },
                {
                    "product": "Testovací produkt 2",
                    "spare_part": [{"code": "P1002", "name": "Testovací příslušenství 2"}]
                },
                {
                    "product": "Testovací produkt 3",
                    "spare_part": [{"code": "P1003", "name": "Testovací příslušenství 3"}]
                }
            ]
        }
        self.assertEqual(self.parser.get_spare_parts(), expected_spare_parts)

if __name__ == '__main__':
    unittest.main()