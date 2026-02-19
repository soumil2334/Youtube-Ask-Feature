FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-distutils \
    python3-pip \
    git \
    wget \
    curl \
    libgl1 \
    libglib2.0-0 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3.10 /usr/bin/python

RUN python -m pip install --upgrade pip

WORKDIR /app

RUN pip install numpy==1.26.4

RUN pip install opencv-python==4.6.0.66

RUN pip install paddlepaddle-gpu==2.6.1

RUN pip install paddleocr==2.7.3

RUN pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 \
    --index-url https://download.pytorch.org/whl/cu121

RUN pip install \
    fastapi==0.128.2 \
    uvicorn==0.40.0 \
    chromadb==1.4.1 \
    langgraph==1.0.8 \
    langchain-core==1.2.11 \
    transformers==5.1.0 \
    sentence-transformers==5.2.2 \
    onnxruntime==1.24.1 \
    redis==7.1.1 \
    yt-dlp==2026.2.4

COPY . .

CMD ["python", "main.py"]
