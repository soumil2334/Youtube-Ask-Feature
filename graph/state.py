from langgraph.graph import StateGraph, END, START
from typing import TypedDict, List, Optional, Annotated
from pathlib import Path
import operator

class AgentState(TypedDict):
    user_message: Optional[str]
    
    router_decision : Optional[str]

    chat_history: Optional[Annotated[List[dict[str, str]], operator.add]]
    knowledge_history : Optional[Annotated[List[str], operator.add]]

    parent_dir:Path
    chroma_path:Path
    collection_name:str

    retrieved_docs : Optional[str]
    ocr_data : Optional[str]

    final_prompt: Optional[str]

    LLM_response : Optional[str]
