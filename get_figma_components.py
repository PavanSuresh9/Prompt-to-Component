from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Update this with your actual Figma access token
FIGMA_ACCESS_TOKEN = "figd_lgQUdVOZ1s4NZ-AWz4ESFQ1EqsceMsSuV5nrnmoj"
# Your file ID from the embedded link
FILE_ID = 'QGn3mkdcs3F27hNz71U88S'  # Replace with your actual file ID

@app.route('/')
def home():
    return "Welcome to the Prompt to Component API!"

@app.route('/get-components', methods=['GET'])
def get_components():
    FILE_ID = 'QGn3mkdcs3F27hNz71U88S'
    url = f"https://api.figma.com/v1/files/{FILE_ID}/components"
    headers = {
        "X-Figma-Token": FIGMA_ACCESS_TOKEN
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        components = response.json().get("meta", {}).get("components", [])
        if components:  # Check if components exist
            return jsonify({"components": components})
        else:
            return jsonify({"message": "No components found."}), 404
    else:
        return jsonify({"error": "Could not fetch components"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True,port=5001)
