import cv2 as cv
from pathlib import Path
import pytesseract
from PIL import Image
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#upload_video/job_id will be parent_directory
def get_frame(i:int, start:int, end:int, parent_dir:Path):
    '''
    i : to represent Document number
    start : starting time of the transcript
    end : ending time of the transcript
    parent_dir : job_id folder
    '''
    
    video_path=f'{parent_dir}/video.mp4'
    mid=(start+end)//2
    cap=cv.VideoCapture(video_path)

    #checking the frames per second
    fps=cap.get(cv.CAP_PROP_FPS)

    frame_index=int(mid*fps)
    current_frame=cap.set(cv.CAP_PROP_POS_FRAMES, frame_index)

    ret, frame=cap.read()
   
    if ret:
        Parent_Dir=Path(parent_dir)
        images_folder=Parent_Dir/'images'
        images_folder.mkdir(parents=True, exist_ok=True)

        cv.imwrite(f'{images_folder}/{i}.jpg', frame)
        return str(f'{images_folder}/{i}.jpg')
    
    else:
        logging.error('Frames not captured')
        raise

def tesseract_OCR(image_path: str):
    try:
        text=pytesseract.image_to_string(Image.open(image_path), lang='eng')
    except Exception as e:
        logging.error(e)
        raise

    return text