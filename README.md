
# 🦊 FileFox - AI Docs Chatbot

**FileFox** is a full-stack AI chatbot that answers questions based on uploaded documents (**PDF, DOCX, CSV**) using a **local LLM** with no API costs.

---

## Features

- Upload & chat with your documents  
- Local AI via **Ollama (phi3:latest)**  
- Smart search with **Qdrant vector DB**  
- Cloud file storage on **DigitalOcean Spaces**  
- Modern UI design  

---

## Tech Stack

**Backend:** FastAPI · Qdrant · Ollama · sentence-transformers · DigitalOcean Spaces  
**Frontend:** React + Vite (deployed on vercel)

---

## Prerequisites

Before you start, install:

- **Python 3.10+**
- **Node.js 18+**
- **Ollama** → [Download here](https://ollama.com/download)

After installing Ollama, pull the model:
```bash
ollama pull phi3:latest, or Llama 3.2:3b (main 2 ollama models recommended for computer with less storage runs smoothly on macbook M1,M2 and windows)

You’ll also need:
	•	Qdrant Cloud (Free)
	•	DigitalOcean Spaces ($5/month) (optional for file storage , you can decide to entirely run it with you local machine storage)


📁 Project Structure

filefox/
├── backend/
│   ├── app.py                 # Main FastAPI app
│   ├── document_parser.py     # Parse PDF/DOCX/CSV
│   ├── embeddings.py          # Generate embeddings
│   ├── qdrant_utils.py        # Vector database operations
│   ├── s3_utils.py            # DigitalOcean Spaces upload
│   ├── llm_client.py          # Ollama integration
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Your secret keys (PLs DON'T COMMIT!)
│
└── frontend/
    ├── src/
    │   ├── App.jsx            # Main React component
    │   ├── App.css            # Styling
    │   ├── main.jsx           # React entry point
    │   └── index.css          # Global styles
    ├── package.json
    └── .env                   # Frontend config (DON'T COMMIT!)
	

	  How It Works

Upload: User uploads a document (PDF, DOCX, or CSV)
Parse: Backend extracts text and splits into chunks
Embed: Each chunk is converted to a vector (embedding)
Store: Vectors are stored in Qdrant, files in DO Spaces
Query: User asks a question
Search: Question is embedded and similar chunks are found
Generate: Ollama generates an answer using retrieved chunks
Display: Answer are shown to user


    Tips & Best Practices
For Better Answers:
Upload documents with clear, well-structured text
Ask specific questions rather than vague ones
If answer is poor, try rephrasing your question

File Guidelines:
PDFs: Works best with text-based PDFs (not scanned images)
DOCX: Plain text documents work best
CSV: Good for structured data, FAQs, etc.

Performance:
First query after upload may be slower (model loading)
Larger files take longer to process
Llama phi3:lastest or 3.2:3b is fast but limited - for better quality, use larger models

Cost Management:
Qdrant free tier: 1GB storage
DO Spaces: $5/month for 250GB
Ollama: 100% free (runs locally)
Total monthly cost: ~$5

**Need Help?** Refer to SETUP_CHECKLIST.md for detailed checklist guide!