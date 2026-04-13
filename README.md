# FileFox — AI Document Analysis Chatbot

### Full-Stack AI Chatbot with Document Upload, Vector Search & CMS Integration

![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi)
![React](https://img.shields.io/badge/Frontend-React%20+%20Vite-61DAFB?logo=react)
![Ollama](https://img.shields.io/badge/LLM-Ollama%20phi3-black)
![Qdrant](https://img.shields.io/badge/VectorDB-Qdrant-red)
![DigitalOcean](https://img.shields.io/badge/Storage-DigitalOcean%20Spaces-0080FF?logo=digitalocean)
![Status](https://img.shields.io/badge/Status-Live-brightgreen)

**Live Demo:** https://filefox-weld.vercel.app

---

## Overview

**FileFox** is a full-stack AI-powered chatbot that allows users to upload documents and ask questions about their content. It uses a **Retrieval-Augmented Generation (RAG)** pipeline which means documents are parsed, chunked, embedded into vectors, and stored in a vector database. When a user asks a question, the most relevant chunks are retrieved and passed to a local LLM to generate a precise, context-aware answer.

Supported file formats: **PDF, DOCX, CSV**

> Built during an internship at **GLP Software, Wrocław** as a practical implementation of local AI, vector search, and cloud storage integration.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup & Installation](#setup--installation)
- [Usage Tips](#usage-tips)
- [Cost Overview](#cost-overview)

---

## Features

- Upload and chat with your own documents (PDF, DOCX, CSV)
- Local AI inference via **Ollama (phi3:latest)** no external API costs
- Semantic search powered by **Qdrant vector database**
- Cloud file storage on **DigitalOcean Spaces**
- Clean, responsive UI which works on desktop and mobile
- **Clear All** button to reset documents and embeddings between sessions
- CMS content integration support

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI |
| **LLM** | Ollama (phi3:latest)  runs locally |
| **Embeddings** | sentence-transformers |
| **Vector Database** | Qdrant Cloud |
| **File Storage** | DigitalOcean Spaces (S3-compatible) |
| **Frontend** | React + Vite |
| **Deployment** | Vercel (frontend) |

---

## How It Works

```
Upload → Parse → Embed → Store → Query → Search → Generate → Display
```

1. **Upload**: User uploads a document (PDF, DOCX, or CSV)
2. **Parse**: Backend extracts and splits text into chunks
3. **Embed**: Each chunk is converted into a vector using sentence-transformers
4. **Store**: Vectors are stored in Qdrant; files are stored in DigitalOcean Spaces
5. **Query**: User asks a question
6. **Search**: Question is embedded and semantically similar chunks are retrieved
7. **Generate**: Ollama generates a context-aware answer using the retrieved chunks
8. **Display**: Answer is shown to the user in the chat interface

---

## Project Structure

```
filefox/
├── backend/
│   ├── app.py                 # Main FastAPI application
│   ├── document_parser.py     # PDF/DOCX/CSV text extraction
│   ├── embeddings.py          # Vector embedding generation
│   ├── qdrant_utils.py        # Qdrant vector DB operations
│   ├── s3_utils.py            # DigitalOcean Spaces file upload
│   ├── llm_client.py          # Ollama LLM integration
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Secret keys (never commit)
│
└── frontend/
    ├── src/
    │   ├── App.jsx            # Main React component
    │   ├── App.css            # Component styling
    │   ├── main.jsx           # React entry point
    │   └── index.css          # Global styles
    ├── package.json
    └── .env                   # Frontend config (API URL never commit)
```

---

## Prerequisites

Before running FileFox, install the following:

- **Python 3.10+**
- **Node.js 18+**
- **Ollama** → [Download here](https://ollama.com/download)

After installing Ollama, pull the model:

```bash
ollama pull phi3:latest
```

> phi3:latest is optimized for machines with limited storage and runs smoothly on MacBook M1/M2 and Windows systems.

You will also need:

- **Qdrant Cloud** account  [Free tier available](https://cloud.qdrant.io)
- **DigitalOcean Spaces** $5/month for 250GB (optional can run with local storage instead)

---

## Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Nnamdi489/filefox.git
cd filefox
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` directory:

```
QDRANT_URL=your_qdrant_cloud_url
QDRANT_API_KEY=your_qdrant_api_key
DO_SPACES_KEY=your_digitalocean_spaces_key
DO_SPACES_SECRET=your_digitalocean_spaces_secret
DO_SPACES_BUCKET=your_bucket_name
DO_SPACES_REGION=your_region
```

Start the backend:

```bash
uvicorn app:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend/` directory:

```
VITE_API_URL=http://localhost:8000
```

> For remote access, replace `localhost` with your ngrok URL.

Start the frontend:

```bash
npm run dev
```

### 4. Start Ollama

```bash
ollama serve
```

---

## Usage Tips

**For better answers:**
- Upload documents with clear, well-structured text
- Ask specific questions rather than vague ones
- If an answer seems off, try rephrasing the question

**File guidelines:**
- PDFs work best with text-based files (not scanned images)
- DOCX files with plain text produce the best results
- CSVs are ideal for structured data, FAQs, and tables

**Performance notes:**
- The first query after upload may be slower due to model loading
- Larger files take longer to process and embed
- phi3:latest is fast but lightweight for higher quality responses, use larger models on a server with at least 1TB storage

**Clear All button:**
Use the Clear All button to remove all uploaded documents and embeddings from Qdrant. This ensures you start fresh when switching between unrelated topics or when old documents are producing mixed results.

---

## Cost Overview

| Service | Cost |
|---|---|
| Qdrant Cloud (free tier) | Free up to 1GB storage |
| DigitalOcean Spaces | ~$5/month for 250GB |
| Ollama | Free runs locally |
| **Total estimated monthly cost** | **~$5/month** |

---

## Additional Resources

Refer to `SETUP_CHECKLIST.md` for a detailed step-by-step setup guide.

---

## Author

**Nnamdi Alor**  
GLP Software, 54-156 Wrocław  
MA, Computer Engineering _Cybersecurity Specialization  
Vistula University, Warsaw  
[LinkedIn](https://www.linkedin.com/in/nnamdi-alor-586664223) | [GitHub](https://github.com/Nnamdi489)