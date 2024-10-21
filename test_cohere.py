import cohere

# Initialize the Cohere client
co = cohere.Client('X1OMJh6PYBccNFVbLqOKPY7VM54fEK3hZoL6ezVn')  # Replace with your actual Cohere API key

# Test Cohere API by generating a simple response
try:
    response = co.generate(
        model='command-xlarge-nightly',  # Using a specific model
        prompt="welcome to api",
        max_tokens=20
    )

    print("API Key is working!")
    print("Generated Text: ", response.generations[0].text)

except cohere.CohereError as e:
    print("Error:", e)
