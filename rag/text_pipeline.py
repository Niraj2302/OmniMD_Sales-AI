import os
import chromadb
from chromadb.utils import embedding_functions

CHROMA_DATA_PATH = "chroma_db"
EMBED_MODEL = "all-MiniLM-L6-v2"

def get_collection():
    client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBED_MODEL)
    return client.get_or_create_collection(name="sales_knowledge", embedding_function=emb_fn)

def retrieve_text(query_text, n_results=3):
    try:
        collection = get_collection()
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        if results['documents'] and len(results['documents'][0]) > 0:
            return "\n".join(results['documents'][0])

        return "No relevant information found in the knowledge base."
    except Exception as e:
        return f"Error during retrieval: {str(e)}"
async def ingest_text_folder(folder_path):
    collection = get_collection()

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Use filename as ID to prevent duplicates
                collection.add(
                    documents=[content],
                    ids=[filename],
                    metadatas=[{"source": "text", "type": "crm_data"}]
                )
    print(f"Successfully indexed text files from {folder_path}")