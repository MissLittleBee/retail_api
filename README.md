# XML Parser
This is a simple Python script that processes an XML file containing product data from AstraModel. The script provides the following functionality:

- Count the total number of products.
- List product names (one per line).
- List spare parts for products that have them.

The script is built using Flask to provide a web interface where users can access the results via HTTP endpoints.

## Features
- Product Count: Displays the total number of products in the XML file.
- Product Names: Lists all product names, one per line.
- Spare Parts: Lists spare parts for products that have them, along with the associated product name.

## Requirements
viz requirements.txt

## How to Use

Run the script using the following command:

`python app.py`

Access the web interface:

Open your browser and go to [http://127.0.0.1:5000/](url)
You will see a simple web interface with links to the following endpoints:

**Product Count: /count
Product Names: /names
Spare Parts: /spare_parts**

## Code Structure
**app.py:** 
The main script that contains the Flask application and the logic for parsing the XML file.

**Testing:**
The script includes unit tests to ensure the functionality works as expected. 
To deploy this script live, you can use a service like Heroku, PythonAnywhere, or any other web hosting service that supports Python and Flask.

**How it can looks like?**
![Screenshot from app](screenshot.png)
Author
Barbora H.

Enjoy using the XML Parser! 
