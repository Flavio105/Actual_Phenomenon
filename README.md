#  Invoice Reimbursement Analyzer & Chatbot Assistant

This project is an intelligent system for automating the analysis of employee reimbursement invoices against HR policy documents and providing an interactive chatbot interface to query the results. It leverages **FastAPI**, **Gradio**, **LLMs (via Groq API)**, and **FAISS vector store** for robust document processing and semantic search.

---

##  Project Overview

The system provides two main functionalities:

1. **Invoice Analysis API** (`/analyze/`):
   - Accepts an HR Policy PDF and a ZIP file of employee invoices.
   - Extracts text, generates invoice-policy compliance prompts, and queries a language model (LLM) to perform analysis.
   - Stores the result along with invoice metadata in a vector store for future querying.

2. **Chatbot API** (`/chat/`):
   - Accepts natural language queries (e.g., "Show invoices for Ramesh with Partially Reimbursed status").
   - Retrieves relevant stored content from the vector store.
   - Constructs a system prompt and gets a contextual response from the LLM.

A **Gradio-based UI** is provided to make the system user-friendly and visually intuitive.

---

##  Installation Instructions

###  Prerequisites
- Python 3.8+
- `git`
- Groq API key (or replace with OpenAI if needed)

### Clone the Repository

```bash
git clone https://github.com/Shrutakeerti/Actual_Phenomenon.git
cd Actual_Phenomenon
```
###  Install Dependencies
```bash
pip install -r requirements.txt
```
### Directory Structure 
```bash
.
├── main.py               # FastAPI backend
├── interface.py          # Gradio frontend
├── prompts.py            # Prompt engineering
├── utils.py              # File parsing utils
├── vector_store.py       # FAISS integration
├── groq_llm.py           # LLM calling logic
├── policy/               # Uploaded HR policies
├── invoices/             # Uploaded ZIP files
```
#  Usage Guide

## ▶ Run the Application

```bash
uvicorn main:app --reload
```
##  Start Gradio UI

In a separate terminal, run:

```bash
python interface.py
```
## 📨 API Endpoints

### `/analyze/` [POST]

**Purpose:**  
Analyze uploaded invoices and store results.

**Payload:**

- `policy_file`: PDF file (UploadFile)  
- `invoice_zip`: ZIP file with invoice PDFs  
- `employee_name`: Employee’s name (Form field)  

**Response:**

```json
{
  "message": "Invoice analysis completed."
}
```
### `/chat/` [POST]

**Purpose:**  
Query stored invoice analysis results.

**Payload:**

- `query`: Natural language string (Form field)

**Response:**

```json
{
  "response": "Ramesh has 3 invoices marked as Partially Reimbursed..."
}
```
## Technical Details
### LLM & Embeddings
### LLM Provider: Groq (via LLaMA3 models)

## Embedding Model: SentenceTransformers (sentence-transformers/all-MiniLM-L6-v2)

### Vector Store
### Backend: Faat API

## Storage Logic:

### Each invoice + LLM summary is saved with metadata (employee name, filename, date).

### Stored as vector embeddings with FAISS for fast retrieval.

## ✍️ Prompt Design

### Invoice Analysis Prompt

**Crafted to:**

- Summarize invoice content  
- Validate against HR policy rules  
- Mark non-compliance if any  

**Prompt Template:**
### Based on the HR policy: {policy_text}
### Analyze this invoice: {invoice_text}

## 💬 Code Comments & Docstrings

### 🗃 `vector_store.py`

```python
def add_to_vector_store(doc_id, content, metadata):
    """
    Converts text to embeddings and stores them with associated metadata in FAISS.
    """
```

### 🤖 Chatbot Logic

```python
async def chat(query: str = Form(...)):
    """
    Retrieves context from FAISS vector store based on query,
    constructs a prompt and sends to LLM.
    """
```
### 🧾 Invoice Analysis

```python
async def analyze(...):
    """
    Unzips invoice PDFs, extracts text, runs compliance check against policy,
    and stores results in vector DB.
    """
```

## Author
### Made with ❤️ by Shrutakeerti

