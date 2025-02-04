import json
import logging
import os
import zipfile
from urllib.request import urlretrieve

from flask import Flask, jsonify, render_template, Response
from lxml import etree

# initializing global logger for this script
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

download_url = "https://www.retailys.cz/wp-content/uploads/astra_export_xml.zip"

class File_manager:
    """
    A class representating downloading and extracting ZIP file
    Atributes:
     file_url - source url for donloading ZIP file
     output_dir - directory for saving output file
    """

    def __init__(self, file_url, output_dir):
        logger.debug(f"Initializing File_manager with file: {file_url}")
        self.file_url = file_url
        self.output_dir = output_dir
        self.zip_path = os.path.join(output_dir, "data.zip")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logger.debug(f"Output directory made in {self.zip_path}")

    def download_zip(self):
        logger.debug(f"Downloading ZIP file from {self.file_url}")
        urlretrieve(self.file_url, self.zip_path)
        logger.info(f"Downloading completed.")

    def extract_zip(self):
        logger.info(f"Zip file extracting...")
        with zipfile.ZipFile(self.zip_path,"r") as zip_ref:
            zip_ref.extractall(self.output_dir)
        logger.info("Extraction completed.")

class ProductParser:
    """
    A class for processing and operating with XML files.
    Atributes:
        xml_file - xml file for parsing
    """
    def __init__(self, xml_file):
        logger.debug(f"Initializing ProductParser with file: {xml_file}")

        if not os.path.exists(xml_file):
            raise FileNotFoundError(f"XML file {xml_file} not found.")

        self.tree = etree.parse(xml_file)
        self.root = self.tree.getroot()

    def get_product_count(self):
        """ Returns totally sum of all products & spare parts in XML file, regardless of duplicate items in the file"""
        count = len(self.root.findall(".//item")) # count all items even with spare parts
        logger.debug(f"Product count: {count}")
        return count

    def get_product_names(self):
        """Returns list of product names & spare parts. without duplicity values """
        names = {item.get('name') for item in self.root.findall(".//item")} # using set for deleting duplicities
        logger.debug(f"Product names: {names}")
        return list(names)

    def get_spare_parts(self):
        """ Returns dictionary of products with their spare parts """
        product_spare_parts = []
        for item in self.root.findall(".//item"):
            product_name = item.get("name")
            spare_parts = item.findall(".//parts//part//item")
            if spare_parts:
                parts_list = []
                for spare_part in spare_parts:
                    parts_list.append({
                        "code": spare_part.get("code"),
                        "name": spare_part.get("name")
                    })
                product_spare_parts.append({
                    "product": product_name,
                    "spare_part": parts_list
                })
        logger.debug(f"Spare parts found: {product_spare_parts}")
        return {"product_spare_parts": product_spare_parts}

def create_app():
    app = Flask(__name__)
    logger.debug("Flask app initialized.")
    output_dir = "data"
    file_manager = File_manager(download_url, output_dir)
    file_manager.download_zip()
    file_manager.extract_zip()

    xml_file = None
    for file in os.listdir(output_dir):
        if file.endswith(".xml"):
            xml_file = os.path.join(output_dir, file)
            break # should be one file in zip file, end after finding first one if there are multiple ones

    if not xml_file:
        raise FileNotFoundError("XML file was not found in extracted ZIP archive.")

    parser = ProductParser(xml_file)

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
        product_names = parser.get_product_names()
        data = {"product_names": product_names}

        json_response = json.dumps(data, ensure_ascii=False, indent=4)

        return Response(
            json_response,
            mimetype='application/json'
        )

    @app.route("/spare_parts", methods=["GET"])
    def get_spare_parts():
        logger.info("App - Spare parts returned.")
        data = {"product_spare_parts": parser.get_spare_parts()}
        json_response = json.dumps(data, ensure_ascii=False, indent=4)

        return Response(
            json_response,
            mimetype='application/json'
        )

    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Starting Flask app.")
    app.run(debug=False) #if true, testing server restarted and run again

app = create_app()