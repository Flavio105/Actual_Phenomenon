import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
# vector store using chromadb and sentence-transformers
model_name = "all-MiniLM-L6-v2"
embedding_function = SentenceTransformerEmbeddingFunction(model_name)
# chromadb client , I have initialized
chroma_client = chromadb.Client()

collection = chroma_client.get_or_create_collection(
    name="invoice_analysis",
    embedding_function=embedding_function
)
# Function to add docs 
def add_to_vector_store(doc_id: str, content: str, metadata: dict):
    collection.add(
        documents=[content],
        ids=[doc_id],
        metadatas=[metadata]
    )
# in this func , querying the vector store
def query_vector_store(query: str, filters: dict = None, k: int = 3):
    if filters and len(filters) > 0:
        results = collection.query(
            query_texts=[query],
            n_results=k,
            where=filters
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=k
        )

    return results['documents'][0] if results['documents'] else []
