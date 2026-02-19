from google import genai
from dotenv import load_dotenv
from graph.state import AgentState
from pydantic import BaseModel

load_dotenv()

client=genai.Client()


def JSON_Model(model_name : str, question: str) -> str:
    response=client.models.generate_content(
        model=model_name,
        contents=question,
        config=genai.types.GenerateContentConfig(
            response_mime_type="application/json"
            )
    )
    return response

def Model(model_name : str, question: str) -> str:
    response=client.models.generate_content(
        model=model_name,
        contents=question,
    )
    return response


