<div align="center">

# 🎬 AskTube

### Chat with any YouTube video using AI

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agent-FF6B6B?style=flat-square)](https://github.com/langchain-ai/langgraph)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Store-orange?style=flat-square)](https://www.trychroma.com)
[![Whisper](https://img.shields.io/badge/OpenAI-Whisper-412991?style=flat-square&logo=openai&logoColor=white)](https://github.com/openai/whisper)

</div>

---

## 📽️ Demo

> **Click the thumbnail below to watch the full project walkthrough on Loom**

<div align="center">

![Watch the demo](https://www.loom.com/share/82c1a6fbd27b4b909d3c82cd5e03db8b)


</div>

---

## 🧠 How It Works

AskTube lets you paste any public YouTube URL, automatically downloads the video, transcribes it using OpenAI Whisper, indexes the transcription into ChromaDB, and exposes a real-time WebSocket chat interface powered by a LangGraph agent — all served via a single FastAPI backend.

```
     YouTube URL
         │
         ▼
┌─────────────────┐
│  yt-dlp / pytube │  ── downloads video.mp4 + audio.wav
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  OpenAI Whisper  │  ── transcribes audio → timestamped segments (.jsonl)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    ChromaDB      │  ── embeds & indexes transcript chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   EasyOCR        │  ── extracts text from video frames & visual content
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LangGraph Agent │  ── routes queries, retrieves context, calls LLM
└────────┬────────┘
         │
         ▼
   WebSocket Chat  ──  real-time responses in the browser
```

---
### 🤖 LangGraph Agent Architecture

The chatbot uses a conditional routing graph to intelligently handle different query types:

![LangGraph Architecture](architecture/output.png)

| Route | Trigger | Behaviour |
|-------|---------|-----------|
| `GeneralQuery` | Casual or off-topic questions | Answers directly without retrieval |
| `History_Only` | Follow-up questions referencing prior context | Uses conversation history only |
| `Retrieval_Required` | Video-specific questions | Fetches relevant transcript chunks from ChromaDB + OCR data before calling the LLM |

---
## 🗂️ Project Structure
```
youtube-ask-feature/
│
├── graph/
│   ├── graph_nodes.py      # LangGraph node definitions & chatbot entrypoint
│   ├── LLM_call.py         # LLM invocation logic
│   └── state.py            # AgentState TypedDict
│
├── static/                 # Static assets served by FastAPI
├── upload_videos/          # Runtime directory for downloaded videos (gitignored)
│
├── main.py                 # FastAPI app — all routes & WebSocket endpoint
├── app.py                  # YouTube download & video processing helpers
├── store_in_DB.py          # ChromaDB ingestion logic
├── OCR.py                  # OCR utilities for visual content
├── transcript_from_audio.py
│
├── frontend2.html          # Single-file frontend (video player + chat UI)
├── Dockerfile
├── requirements.txt
└── .env                    # API keys (never commit this)
```

---

## ✨ Features

- **One-click YouTube ingestion** — paste a URL and the pipeline runs automatically
- **In-browser video playback** — watch the video alongside your conversation
- **Real-time AI chat via WebSockets** — no page reloads, responses stream live
- **Timestamped retrieval** — the agent retrieves semantically relevant transcript segments
- **LangGraph multi-node agent** — router decides between RAG retrieval and direct response
- **Persistent vector store** — ChromaDB persists per-job so you can re-query without re-indexing
- **Fully Dockerized** — one command to run everything

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/) installed
- An NVIDIA GPU is **strongly recommended** for Whisper transcription speed (CUDA 11.8+)
- A valid OpenAI (or compatible) API key

---

### Option 1 — Docker (Recommended)

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/youtube-ask-feature.git
cd youtube-ask-feature
```

**2. Create your `.env` file**

```bash
cp .env.example .env   # or create it manually
```

Edit `.env` and fill in your keys:

```env
OPENAI_API_KEY=sk-...
# Add any other keys your LLM_call.py or graph nodes require
```

**3. Build and run**

```bash
docker compose up --build
```

> If you don't have a `docker-compose.yml` yet, run the container directly:

```bash
# Build the image
docker build -t asktube .

# Run with GPU support
docker run --gpus all -p 8000:8000 --env-file .env asktube

# Run without GPU (Whisper will use CPU — slower)
docker run -p 8000:8000 --env-file .env asktube
```

**4. Open the app**

```
http://localhost:8000
```

---

### Option 2 — Local Python (without Docker)

**1. Clone and create a virtual environment**

```bash
git clone https://github.com/YOUR_USERNAME/youtube-ask-feature.git
cd youtube-ask-feature

python -m venv myenv
source myenv/bin/activate        # Windows: myenv\Scripts\activate
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

> **CUDA users:** Make sure your PyTorch install matches your CUDA version.
> Visit [pytorch.org/get-started](https://pytorch.org/get-started/locally/) and install the matching wheel before running pip install.

**3. Set up environment variables**

```bash
cp .env.example .env
# Edit .env with your API keys
```

**4. Run the server**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**5. Open the app**

```
http://localhost:8000
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the frontend HTML |
| `POST` | `/upload-url?url=<yt_url>` | Downloads YouTube video, returns `job_id` |
| `GET` | `/status/{job_id}` | Poll processing status: `processing` / `ready` / `failed` |
| `POST` | `/upload/{job_id}` | Transcribe audio → embed → store in ChromaDB |
| `WS` | `/upload/{job_id}/query` | WebSocket chat endpoint |
| `DELETE` | `/uploads/{job_id}/delete` | Clean up all files for a job |
| `GET` | `/videos/{job_id}/video.mp4` | Serve the downloaded video file |

---

## ⚙️ Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your LLM provider API key | required |
| `WHISPER_MODEL` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large`) | `base` |
| `UPLOAD_DIR` | Directory for storing video/audio/transcripts | `upload_videos/` |

Change the Whisper model size in `main.py`:

```python
model = whisper.load_model("base", device='cuda')  # change "base" → "medium" for better accuracy
```

---

## 🐳 Dockerfile Notes

The included `Dockerfile` sets up:
- Python base image with CUDA support
- `ffmpeg` for audio extraction
- All Python dependencies from `requirements.txt`
- Exposes port `8000`

If your base image doesn't include CUDA and you want GPU transcription, change the first line of your Dockerfile to:

```dockerfile
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04
```

And ensure you pass `--gpus all` when running the container.

---

## 🛠️ Troubleshooting

**Video not loading after URL submission**
- Make sure the YouTube URL is public and not age-restricted
- Check `upload_videos/{job_id}/` exists and contains `video.mp4`

**Transcription is very slow**
- You're running on CPU. Pass `--gpus all` to Docker or install a CUDA-compatible PyTorch

**WebSocket disconnects immediately**
- Ensure you called `POST /upload/{job_id}` first — chat is only available after indexing
- Check that ChromaDB directory was created at `upload_videos/{job_id}/chromaDB/`

**ChromaDB errors on startup**
- Delete stale `upload_videos/` directories from previous runs and restart

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">
Built with FastAPI · LangGraph · OpenAI Whisper · ChromaDB
</div>
