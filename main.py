from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pathlib import Path
import torch
import ffmpeg
import logging
import shutil
import uuid
import whisper
import json
import logging

from app import download_yt, process_video
from store_in_DB import create_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

UPLOAD_DIR=Path('uplaod_videos')
UPLOAD_DIR.mkdir(exist_ok=True)

app=FastAPI()

model = whisper.load_model("base", device='cuda')

# About def upload_url
#1.Uploading Youtube video url -> receives seperate audio and video
#2.Extracting audio from video
#3.Creating transcription from audio
@app.post("/upload-url")
async def upload_url(bg:BackgroundTasks,url:str):
    job_id=str(uuid.uuid4())
    parent_dir=UPLOAD_DIR/job_id
    parent_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        download_yt(parent_dir, url)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail='Error while downloading youtube video'
        )
    video_path=parent_dir/'video.mp4'
    bg.add_task(process_video, UPLOAD_DIR, video_path, job_id)
    
    return JSONResponse(
        status_code=200,
        content={
            'job_id':job_id,
            'status':'In Process'
        }
    )

@app.post("/upload/{job_id}")
async def save_DB(job_id:str):
    audio_path=UPLOAD_DIR/job_id/'audio.wav'
    if not audio_path.exists():
        raise FileNotFoundError(f'Audio file not found for job {job_id}')
    try:
        #result is a dictionary
        result = model.transcribe(str(audio_path))
        logging.info('transcription completed')
        segments=result['segments']

        if not result:
            raise ValueError("Transcription is empty or failed")
    
        parent_dir=UPLOAD_DIR/job_id
        if parent_dir.exists():
            logging.info('Parent Directory exists')
            text_path=parent_dir/'transcript.jsonl'
        else:
            logging.error("Parent directory doesn't exist")
            parent_dir.mkdir(parents=True, exist_ok=True)
            text_path=parent_dir/'transcript.jsonl'
        
        with open(text_path, 'w', encoding='utf-8') as f:
            for segment in segments:
                temp_dict={'start': segment['start'], 'end': segment['end'], 'text': segment['text']}       
                json_line = json.dumps(temp_dict, ensure_ascii=False)
                f.write(json_line + "\n")
        
        ChromaDB_dir=create_db(UPLOAD_DIR, job_id)
        
        return JSONResponse(
            status_code=200,
            content={
            'job_id':job_id,
            'Chroma DB': ChromaDB_dir}
        )
    
    except Exception as e:
        logging.error(f'{e}')
        raise HTTPException(
            status_code=500
        )

@app.post('/chat/{collection_name}')
async def chat(bg: BackgroundTasks, collection_name: str):
    

#Delteing the job_id folder once task performed

@app.delete("/uploads/{job_id}/delete")
async def delete_job(job_id:str):
    job_dir=UPLOAD_DIR/job_id
    if not job_dir.exists():
        raise HTTPException(
            status_code=404,
            detail=f'{job_dir} not found'
        )
    
    try:
        shutil.rmtree(job_dir)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'Unexpected error occurred : {e}'
        )
    return JSONResponse(
        status_code=200,
        content={
            'job id': f'{job_id}',
            'status':'job delted'
        }
    )