import os
import anthropic
from dotenv import load_dotenv
import chromadb
from chromadb.utils import embedding_functions

# Load environment variables from .env file
load_dotenv()


# Retrieve Anthropic API key from environment variables
claudeai_api_key = os.getenv("ANTHROPIC_API_KEY")  # Standard naming

# Initialize ChromaDB client (fix the syntax)
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Note: Anthropic doesn't provide embedding functions for ChromaDB
# You should use a different embedding function
default_ef = embedding_functions.DefaultEmbeddingFunction()


collection = chroma_client.get_or_create_collection(
    name="my_collection",
    embedding_function=default_ef,
)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=claudeai_api_key)

# Fix the API call - Anthropic uses different syntax
message = client.messages.create(
    model="claude-sonnet-4-20250514",  # Use current model
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(message.content[0].text)

