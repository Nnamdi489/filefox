
#  FileFox Setup Checklist

Use this checklist to make sure you've completed all setup steps correctly.

## Pre-Installation Checklist

- [ ] Python 3.10+ installed (`python --version`)
- [ ] Node.js 18+ installed (`node --version`)
- [ ] Git installed (`git --version`)
- [ ] Text editor installed (VS Code, Sublime, etc.)

## Account Setup Checklist

### Qdrant Cloud
- [ ] Account created at https://cloud.qdrant.io/
- [ ] Free cluster created
- [ ] Cluster URL copied (format: `https://xxxxx.cloud.qdrant.io`)
- [ ] API key copied from dashboard

### DigitalOcean Spaces
- [ ] Account created at https://digitalocean.com
- [ ] Space created (note the region, e.g., `fra1`)
- [ ] Spaces access key generated
- [ ] Spaces secret key saved
- [ ] Bucket name noted
- [ ] Endpoint URL noted (e.g., `https://fra1.digitaloceanspaces.com`)

### Ollama
- [ ] Ollama downloaded from https://ollama.com/download
- [ ] Ollama installed
- [ ] Model pulled: `ollama pull llama3.2:3b` or `pull phi3:latest`
- [ ] Ollama tested: `ollama list` shows llama3.2:3b or phi3:latest

## Backend Setup Checklist

- [ ] Navigated to project: `cd filefox/backend`
- [ ] Virtual environment created: `python -m venv venv`
- [ ] Virtual environment activated:
  - Mac/Linux: `source venv/bin/activate`
 - [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] `.env.example` copied to `.env`: `cp .env.example .env`
- [ ] `.env` file edited with actual credentials
- [ ] All environment variables filled in:
  - [ ] `QDRANT_URL`
  - [ ] `QDRANT_API_KEY`
  - [ ] `DO_SPACES_KEY`
  - [ ] `DO_SPACES_SECRET`
  - [ ] `DO_SPACES_ENDPOINT`
  - [ ] `DO_SPACES_BUCKET`
  - [ ] `DO_SPACES_REGION`
  - [ ] `OLLAMA_BASE_URL`
  - [ ] `OLLAMA_MODEL`

##  Frontend Setup Checklist

- [ ] Navigated to frontend: `cd filefox/frontend`
- [ ] Dependencies installed: `npm install`
- [ ] `.env.example` copied to `.env`: `cp .env.example .env`
- [ ] `.env` file contains correct API URL:
  - For local: `VITE_API_URL=http://localhost:8000`
  - For ngrok: `VITE_API_URL=https://your-ngrok-url.ngrok-free.app`

## First Run Checklist

### Terminal 1: Ollama
- [ ] Ollama started: `ollama serve`
- [ ] Terminal shows "Listening on ..."
- [ ] Left running in background

### Terminal 2: Backend
- [ ] In backend folder: `cd backend`
- [ ] Virtual env activated: `source venv/bin/activate`
- [ ] Backend started: `uvicorn app:app --reload --port 8000`
- [ ] No error messages in output
- [ ] Shows "Uvicorn running on http://127.0.0.1:8000"
- [ ] Can access http://localhost:8000 in browser

### Terminal 3: Frontend
- [ ] In frontend folder: `cd frontend`
- [ ] Frontend started: `npm run dev`
- [ ] Shows "Local: http://localhost:5173/"
- [ ] Can access http://localhost:5173 in browser
- [ ] FileFox welcome screen visible

## Functionality Testing

- [ ] Upload test:
  - [ ] Click 📎 button
  - [ ] Select a test PDF/DOCX/CSV file
  - [ ] See "✓ uploaded successfully" message
  - [ ] No errors in browser console 

- [ ] Query test:
  - [ ] Type a question about uploaded document
  - [ ] Press Enter or click send button (↑)
  - [ ] See loading indicator 
  - [ ] Receive an answer
 
##  ngrok Setup Checklist

- [ ] ngrok account created at https://ngrok.com
- [ ] ngrok downloaded and installed
- [ ] Auth token configured: `ngrok config add-authtoken YOUR_TOKEN`
- [ ] ngrok started: `ngrok http 8000`
- [ ] ngrok URL copied (the https:// one)
- [ ] Frontend `.env` updated with ngrok URL
- [ ] Frontend restarted after `.env` change

##  Deployment Checklist (Optional)

### Vercel Deployment
- [ ] Code pushed to GitHub
- [ ] Vercel account created
- [ ] New project created in Vercel
- [ ] GitHub repo connected
- [ ] Root directory set to `frontend`
- [ ] Environment variable added:
  - Key: `VITE_API_URL`
  - Value: Your backend URL (your ngrok backend URL)
- [ ] Deployment successful
- [ ] Can access deployed frontend
- [ ] Upload and query work on deployed version


## 🎉 Success Criteria

You're done when:
- You can upload a document
- You can ask questions about it
- You get meaningful answers
- No errors in console or logs


