import cv2 as cv
from pathlib import Path
from paddleocr import PaddleOCR

def get_frame(i:int, start:int, end:int, parent_dir:str):
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
   
    if not ret:
        Parent_Dir=Path(parent_dir)
        images_folder=Parent_Dir/'images'
        images_folder.mkdir(parents=True, exist_ok=True)

        cv.imwrite(f'{images_folder}/{i}.jpg', frame)
        return str(f'{images_folder}/{i}.jpg')
    
    else:
        return None

def perform_OCR(image_path:str):
    if not image_path:
        return None
    
    image=cv.imread(image_path)
    if image:
        #removing colour as in OCR colour is not required
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        gray = cv.adaptiveThreshold(
            gray, 255,
            cv.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv.THRESH_BINARY,
            31, 2)
        
        ocr = PaddleOCR(
            use_angle_cls=True,  #handles rotated text
            lang='en'            #change if needed
        )
        ocr_text=[]    
        result=ocr.predict(gray, cls=True)
        
        for line in result[0]:
            bbox=line[0]
            text=line[1][0]
            confidence= line[1][1]
            
            #appending the recognized text along with 
            #the confidence and the bbox region it is 
            #present within
            ocr_text.append({
                'text': text,
                'confidence': confidence,
                'bbox':bbox
            })
        
        final_text=','.join(
            text['text'] for text in ocr_text if text['confidence'] > 0.7
            )
        return final_text
    else:
        return None
        
