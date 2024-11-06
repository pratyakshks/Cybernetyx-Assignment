from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List
from chromadb import Client as ChromaClient
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import asyncio
import os
from io import BytesIO
from docx import Document
from PyPDF2 import PdfReader
import uuid

app = FastAPI()

# Initialize ChromaDB client and embedding model
chroma_client = ChromaClient()
collection_name = "documents"
if collection_name not in chroma_client.list_collections():
    chroma_client.create_collection(collection_name)
collection = chroma_client.get_collection(collection_name)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Helper functions to extract text
async def extract_text(file: UploadFile) -> str:
    file_content = await file.read()
    if file.filename.endswith(".pdf"):
        return extract_text_from_pdf(BytesIO(file_content))
    elif file.filename.endswith(".doc") or file.filename.endswith(".docx"):
        return extract_text_from_docx(BytesIO(file_content))
    elif file.filename.endswith(".txt"):
        return file_content.decode("utf-8")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")

def extract_text_from_pdf(file) -> str:
    pdf_reader = PdfReader(file)
    return "\n".join(page.extract_text() for page in pdf_reader.pages if page.extract_text())

def extract_text_from_docx(file) -> str:
    doc = Document(file)
    return "\n".join(paragraph.text for paragraph in doc.paragraphs)

# Data models for request and response
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class DocumentResponse(BaseModel):
    content: str
    score: float

@app.post("/ingest")
async def ingest_document(file: UploadFile):
    # Extract text from the uploaded file
    text = await extract_text(file)
    
    # Generate the embedding for the extracted text
    embedding = model.encode(text, convert_to_tensor=False).tolist()
    
    # Generate a unique document ID
    document_id = f"{file.filename}-{os.urandom(4).hex()}"
    
    # Prepare the data to be added to the collection
    # Ensure the ID, embedding, and content are properly structured
    collection.add(
        ids=[document_id],                # List of document IDs
        embeddings=[embedding],            # List of document embeddings
        documents=[text]                  # List of document contents (text)
    )
    
    return {"message": "Document ingested successfully.", "document_id": document_id}

@app.post("/query")
async def query_documents(query_request: QueryRequest):
    query = query_request.query
    top_k = query_request.top_k
    
    # Perform the search operation
    results = search_documents(query, top_k)
    
    # Prepare response with document content and other details
    response = [
        {"document_id": result["id"], "content": result["content"], "score": result["score"]}
        for result in results
    ]
    
    return {"documents": response}

def search_documents(query: str, top_k: int = 5):
    # Generate the embedding for the query
    query_embedding = model.encode(query, convert_to_tensor=False).tolist()
    print(f"Query Embedding: {query_embedding}")  # Debugging line

    # Perform a similarity search on the collection using the query embedding
    search_results = collection.query(
        query_embeddings=[query_embedding],  # The query embedding
        n_results=top_k  # Number of results to return
    )
    print(f"Search Results: {search_results}")  # Debugging line

    # Check if the search_results contains 'documents' and 'distances'
    if 'documents' not in search_results or 'distances' not in search_results:
        raise HTTPException(status_code=500, detail="Invalid response from ChromaDB.")

    # Extract the results from the search response
    results = []
    for doc, score in zip(search_results['documents'], search_results['distances']):
        # Ensure doc and score are in the expected format
        print(f"Document: {doc}, Score: {score}")  # Debugging line
        if doc and score:  # Ensure both are not empty
            results.append({"id": str(uuid.uuid4()), "content": doc, "score": score})
        else:
            print("Empty document or score found.")  # Debugging line

    return results


@app.get("/")
async def root():
    return {"message": "Welcome to ChromaDB!"}

@app.get("/documents")
async def get_documents():
    all_docs = collection.get()
    return {"documents": all_docs}


# Run server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
