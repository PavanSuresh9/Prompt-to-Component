# Prompt to Component

## Project Overview

**Prompt to Component** is a web application that converts user prompts into pre-designed Figma components. The application interacts with the Figma API and uses AI services like Cohere to generate and retrieve component details based on user inputs.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Challenges](#challenges)
8. [Future Enhancements](#future-enhancements)

## Features

- Users can input component names (e.g., "Primary Button," "Secondary Button") and the application will retrieve the corresponding components from Figma.
- The application integrates with AI services (like Cohere) to enhance the user input and generate detailed prompts.
- The user interface allows the interactive preview of the components retrieved from Figma.

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Figma API**: To retrieve design components
- **Cohere API**: For AI-based prompt generation
- **Neo4j**: For storing and managing component relationships
- **Postman**: For testing API endpoints

## Installation

### Prerequisites
- Python 3.x
- Node.js (for front-end development if needed)
- Figma API Key
- Cohere API Key
- Neo4j running locally or on a cloud server

### Setup Instructions
1. Clone the repository.
    ```bash
    git clone https://github.com/your-username/prompt-to-component.git
    cd prompt-to-component
    ```
2. Create a virtual environment and install the dependencies:
    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```
3. Set up environment variables for Figma and Cohere API keys in a `.env` file:
    ```
    FIGMA_API_KEY=your_figma_api_key
    COHERE_API_KEY=your_cohere_api_key
    ```

4. Run the Flask server:
    ```bash
    python app.py
    ```

5. Test the application locally by visiting `http://127.0.0.1:5000`.

## Usage

1. Once the Flask app is running, you can open a browser and access the application.
2. Input the component name (e.g., "Primary Button") in the provided field.
3. Click the "Generate" button to retrieve the component details.
4. The application will show the retrieved component from Figma, allowing for an interactive preview.

## API Endpoints

### POST `/generate`
- **Description**: Takes the component name as input and generates the corresponding design component from Figma.
- **Request Body**:
    ```json
    {
      "component_name": "Primary Button"
    }
    ```
- **Response**: Returns the Figma component's details such as name, ID, and preview.

### Sample Request:
```bash
curl -X POST http://127.0.0.1:5000/generate -H "Content-Type: application/json" -d '{"component_name": "Primary Button"}'
