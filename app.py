from yt_dlp import YoutubeDL
from pathlib import Path
import logging
import ffmpeg


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def download_yt(video_dir, url:str):
    ydl_opts = {
        "ffmpeg_location": r"C:/ffmpeg/bin",  
        "format": "bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "outtmpl": str(video_dir/"video.%(ext)s"),
        "postprocessor_args": [
        "-c:a", "aac", #apc integration with mp4 doesn't work well so audio converted into aac
        "-b:a", "192k"],
        }
    logging.info('Downloading Youtube video')
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def process_video(UPLOAD_DIR, video_path, job_id:str):
    audio_dir= UPLOAD_DIR/job_id
    audio_dir.mkdir(parents=True, exist_ok=True)

    audio_path=audio_dir/'audio.wav'

    if not video_path.exists():
        raise ValueError("Video file doesn't exist")

    try:
        (
            ffmpeg
            .input(str(video_path))
            .output(
                str(audio_path),
                format='wav',
                acodec="pcm_s16le",
                ac=1,
                ar=16000).overwrite_output().run(capture_stdout=True, capture_stderr=True))
    
    except ffmpeg.Error as e:
        raise ValueError(f"Error {e} occurred")
    pass