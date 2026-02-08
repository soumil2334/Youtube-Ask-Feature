import chromadb
import json
import uuid
from pathlib import Path


def create_db(UPLOAD_DIR, job_id:str):
    chroma_DB=UPLOAD_DIR/job_id/'chromaDB'
    chroma_DB.mkdir(parents=True, exist_ok=True)

    client=chromadb.PersistentClient(path=chroma_DB)
    collection=client.get_or_create_collection(name='transcription')

    transcription=UPLOAD_DIR/job_id/'transcript.jsonl'

    data=[]
    metadata=[]
    with open(transcription, 'r', encoding='utf-8') as f:
        for line in f:
            obj=json.loads(line)
            text=obj['text']
            line_metadata={'start':obj['start'], 'end':obj['end']}
            data.append(text)
            metadata.append(line_metadata)

    collection.add(
        ids=[str(uuid.uuid4()) for _ in data],
        documents=data,
        metadatas=metadata
    )
    chromaDB_dir={
        'chroma_path':'chromaDB',
        'collection_name': 'transcription'
    }
    return chromaDB_dir