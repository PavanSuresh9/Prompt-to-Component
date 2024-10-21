# testneo4j.py

from neo4j import GraphDatabase

# Replace with your actual Neo4j password
neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "12345678"))

def test_connection():
    try:
        with neo4j_driver.session() as session:
            result = session.run("MATCH (n) RETURN n LIMIT 1")
            for record in result:
                print(record)
        print("Connection to Neo4j successful!")
    except Exception as e:
        print(f"Error connecting to Neo4j: {e}")
    finally:
        neo4j_driver.close()

if __name__ == "__main__":
    test_connection()
