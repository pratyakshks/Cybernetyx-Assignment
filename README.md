# FastAPI_ChromaSearch
As a take-home task, we propose implementing a lightweight FastAPl server for RAG. This server should utilize ChromaDB's persistent client for ingesting and querying documents (PDE DOC, DOCX, TXT). Leverage sentence-transformers/all-MiniLM-L6-v2 (CPU) from Hugging Face for embeddings.


# Steps

S-1) Create a virtual environment
        `python -m venv venv`

S-2) Activate Virtual Environment
        `.\venv\Scripts\activate`

S-3) Install packages
        `pip install -r requirements.txt`

S-4) Run FastAPI server
        `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`