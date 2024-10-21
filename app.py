from flask import Flask, request, jsonify
from neo4j import GraphDatabase
import requests

# API Keys and Figma details
COHERE_API_KEY = "X1OMJh6PYBccNFVbLqOKPY7VM54fEK3hZoL6ezVn"  # Your Cohere API key
FIGMA_ACCESS_TOKEN = "figd_lgQUdVOZ1s4NZ-AWz4ESFQ1EqsceMsSuV5nrnmoj"  # Your Figma token
FIGMA_FILE_ID = "ZLYlFFxCqfHggWGRJjkSyh"  # Your Figma file ID

# Initialize Flask app
app = Flask(__name__)

# Initialize Neo4j Driver
neo4j_driver = GraphDatabase.driver(
    "bolt://localhost:7687", 
    auth=("neo4j", "12345678")  # Replace with your actual Neo4j password
)

# Function to generate prompt with Cohere API
def generate_prompt_with_cohere(component_name):
    url = "https://api.cohere.ai/generate"
    
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "command-xlarge-nightly",
        "prompt": f"Generate a Figma design component for {component_name}.",
        "max_tokens": 100,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        result = response.json()
        return result.get("generations")[0]["text"]
    else:
        return f"Error: {response.status_code}, {response.json()}"

# Function to retrieve Figma components by name
def get_figma_components(component_name):
    url = f"https://api.figma.com/v1/files/{FIGMA_FILE_ID}/components"
    headers = {
        "X-Figma-Token": FIGMA_ACCESS_TOKEN
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        components = response.json().get("meta", {}).get("components", [])
        for component in components:
            if component['name'] == component_name:
                return component
    return None

# Function to save components to Neo4j
def save_component_to_neo4j(component_name, component_id):
    with neo4j_driver.session() as session:
        query = """
        MERGE (c:Component {name: $name, id: $component_id})
        RETURN c
        """
        session.run(query, name=component_name, component_id=component_id)

# New route for root URL to display welcome message
@app.route('/')
def home():
    return jsonify({"message": "The component does not exist in the Figma file or an invalid component name is entered"})

# Flask route to generate and store component
@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    component_name = data.get('component_name')

    if not component_name:
        return jsonify({"error": "No component name provided."}), 400

    # Get the component from Figma
    figma_component = get_figma_components(component_name)

    if figma_component:
        component_id = figma_component['key']
        # Save the component to Neo4j
        save_component_to_neo4j(component_name, component_id)

        response = {
            "message": "Component found and saved successfully!",
            "component": figma_component
        }
    else:
        # Generate prompt using Cohere
        generated_prompt = generate_prompt_with_cohere(component_name)
        
        response = {
            "error": "Component not found in Figma. Here's a generated prompt for your component.",
            "generated_prompt": generated_prompt
        }

    return jsonify(response)

# New Endpoint to retrieve component details from Neo4j
@app.route('/component', methods=['GET'])
def get_component():
    component_name = request.args.get('component_name')

    if not component_name:
        return jsonify({"error": "No component name provided."}), 400

    # Query Neo4j for the component details
    with neo4j_driver.session() as session:
        query = """
        MATCH (c:Component {name: $name})
        RETURN c.name as name, c.id as id
        """
        result = session.run(query, name=component_name)
        component = result.single()

        if component:
            return jsonify({
                "component_name": component["name"],
                "component_id": component["id"]
            })
        else:
            return jsonify({"error": "Component not found."}), 404

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)
