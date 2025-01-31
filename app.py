from flask import Flask, jsonify, render_template, Response
import json
from lxml import etree
import logging

# initializing global logger for this script
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

class ProductParser:
    """
    A class for processing and operating with XML files.
    Atributes:
        xml_file - xml file for parsing
    """
    def __init__(self, xml_file):
        logger.debug(f"Initializing ProductParser with file: {xml_file}")
        self.tree = etree.parse(xml_file)
        self.root = self.tree.getroot()

    def get_product_count(self):
        count = len(self.root.findall(".//item"))
        logger.debug(f"Product count: {count}")
        return count

    def get_product_names(self):
        names = [item.get('name') for item in self.root.findall(".//item")]
        logger.debug(f"Product names: {names}")
        return names

    def get_spare_parts(self):
        spare_parts = []
        for item in self.root.findall(".//item"):
            spare_part = item.find(".//parts")
            if spare_part is not None:
                spare_parts.append({
                    "product": item.get("name"),
                    "spare_part": spare_part.text
                })
        logger.debug(f"Spare parts found: {spare_parts}")
        return spare_parts

def create_app(xml_file="export_full.xml"):
    app = Flask(__name__)
    parser = ProductParser(xml_file)  # Inicializace ProductParser uvnitř create_app

    @app.route("/")
    def index():
        logger.info("Home page accessed.")
        return render_template('index.html')

    @app.route("/count", methods=["GET"])
    def count_products():
        logger.info("App - Products counted.")
        return jsonify({"product_count": parser.get_product_count()})

    @app.route("/names", methods=["GET"])
    def names():
        logger.info("App - Product names returned.")
        data = {"product_names": parser.get_product_names()}
        return Response(
            json.dumps(data, ensure_ascii=False),
            mimetype='application/json'
        )

    @app.route("/spare_parts", methods=["GET"])
    def get_spare_parts():
        logger.info("App - Spare parts returned.")
        data = {"product_spare_parts": parser.get_spare_parts()}
        return Response(
            json.dumps(data, ensure_ascii=False),
            mimetype='application/json'
        )

    return app

if __name__ == '__main__':
    app = create_app()  # Vytvoření aplikace s výchozím XML souborem
    logger.info("Starting Flask app.")
    app.run(debug=True)