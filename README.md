
# 🦊 FileFox (web chatbot with document analysis and cms integration)

**Live Demo:** https://filefox-weld.vercel.app (Try FileFox live!)

**FileFox** is a full stack AI chatbot that answers questions based on uploaded documents/files (**PDF, DOCX, CSV**) and CMS content using a vector db and local llm (phi3).

---

## Features

- Upload & chat with your documents  
- Local AI via **Ollama (phi3:latest)**  
- Smart search with **Qdrant vector DB**  
- Cloud file storage on **DigitalOcean Spaces**  
- Modern and responsive design (works on desktop and mobile).


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
ollama pull phi3:latest (ollama model recommended for computer with less storage runs smoothly on macbook M1,M2 and windows)

You’ll also need:
	•	Qdrant Cloud (Free)
	•	DigitalOcean Spaces ($5/month) (optional for file storage , you can decide to entirely run it with your local machine storage)


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
│   └── .env                   # Your secret keys (don't commit , it should be on your .gitignore)
│
└── frontend/
    ├── src/
    │   ├── App.jsx            # Main React component
    │   ├── App.css            # Styling
    │   ├── main.jsx           # React entry point
    │   └── index.css          # styles
    ├── package.json
    └── .env                   # Frontend config (vite_api-url, it can either by default localhost or ngrok please don't commit)
	

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
Llama phi3:lastest is fast but limited - for better quality, use larger models (preferable on a server with atleast 1Tb storage)

Cost Management:
Qdrant free tier: 1GB storage
DO Spaces: $5/month for 250GB
Ollama: free (runs locally)
Total monthly cost: ~$5

🗑️ Using the Clear All Button

The Clear All button in FileFox ensures you start fresh by removing all uploaded documents and embeddings from the Qdrant database. Use it when switching between unrelated topics or when old files cause mixed or irrelevant answers. After clearing, you can safely upload new documents and get responses only from them.

Use when: switching topics, starting a new project, or fixing irrelevant results.


**Need Help?** Refer to SETUP_CHECKLIST.md for detailed checklist guide!