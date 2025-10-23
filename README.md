
# 🦊 FileFox - AI Document Chatbot

**FileFox** is a full-stack AI chatbot that answers questions based on uploaded documents (**PDF, DOCX, CSV**) using a **local LLM** with no API costs.

---

## ✨ Features

- 📄 Upload & chat with your documents  
- 🤖 Local AI via **Ollama (phi3:latest)**  
- 🔍 Smart search with **Qdrant vector DB**  
- 💾 Cloud file storage on **DigitalOcean Spaces**  
- 🎨 Modern matte-black UI with pink accents  

---

## 🛠️ Tech Stack

**Backend:** FastAPI · Qdrant · Ollama · sentence-transformers · DigitalOcean Spaces  
**Frontend:** React + Vite (deployed on vercel)

---

## 📋 Prerequisites

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
