# FastAPI ChromaSearch

This project is a lightweight FastAPI server for Retrieval-Augmented Generation (RAG) using ChromaDB as a vector store for document ingestion and querying. It leverages the `sentence-transformers/all-MiniLM-L6-v2` model from Hugging Face to generate embeddings, allowing for semantic search on documents in PDF, DOCX, and TXT formats.


## Getting Started

Follow these steps to set up and run the FastAPI server on your local machine.

### Steps

S1) **Create a virtual environment**
        `python -m venv venv`

S2) **Activate Virtual Environment**
        `.\venv\Scripts\activate`

S3) **Install packages**
        `pip install -r requirements.txt`

S4) **Run FastAPI server**
        `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
