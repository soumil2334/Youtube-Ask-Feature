import chromadb
import json
import uuid
from pathlib import Path
from chromadb.utils import embedding_functions
import logging
from OCR import get_frame, tesseract_OCR

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s"
)

def create_db(Parent_Dir:Path, job_id:str, collection_name:str):
    chroma_DB=Parent_Dir/'chromaDB'
    chroma_DB.mkdir(parents=True, exist_ok=True)

    client=chromadb.PersistentClient(path=chroma_DB)
    collection=client.get_or_create_collection(name=collection_name)

    transcription=Parent_Dir/'transcript.jsonl'

    data=[]
    metadata=[]

    with open(transcription, 'r', encoding='utf-8') as f:
        for line in f:
            obj=json.loads(line)
            text=obj['text']
            line_metadata={'start':int(obj['start']), 'end':int(obj['end'])}
            data.append(text)
            metadata.append(line_metadata)

    collection.add(
        ids=[str(uuid.uuid4()) for _ in data],
        documents=data,
        metadatas=metadata
    )
    chromaDB_dir={
        'chroma_path':'chromaDB'
    }
    return chromaDB_dir

def query(question: str, collection_name : str, collection_path: Path)-> dict:
    client=chromadb.PersistentClient(path=collection_path)
    logging.info('Chroma client created for query')
    collection=client.get_or_create_collection(name=collection_name)
    logging.info('Chroma collection found')
    try:
        query_result=collection.query(
            query_texts=question,
            n_results=7
        )
        logging.info(f'Query result {query_result}')
        if query_result:
            return dict(query_result)
        else:
            logging.error('Query did not return anything')
            raise
    
    except Exception as e:
        logging.error(f'Error occurred {e}')
        raise

def perform_OCR(query_result: dict, parent_dir:Path):
    ocr_data=[]
    metadatas=query_result['metadatas']
    for i, metadata in enumerate(metadatas[0]):
        start=metadata['start']
        end=metadata['end']
        try:
            frame_path=get_frame(int(i), start, end, parent_dir)
            logging.info('Frame retrieved from video')
            ocr_text=tesseract_OCR(str(frame_path))
            logging.info('OCR performed')
            ocr_data.append(ocr_text)
        except Exception as e:
            logging.error(e)
            raise
    return ocr_data

    

    