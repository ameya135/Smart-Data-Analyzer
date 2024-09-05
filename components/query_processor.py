from haystack import component
import sys
import os
from model.llm import model_response 
import instructor 
from pydantic import BaseModel
from openai import OpenAI
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class QueryFormat(BaseModel):
    query: str
    
@component
class QueryProcessor:
    """
    A component to process the query and return the result.
    """
    client = instructor.from_openai(OpenAI(api_key="ollama", base_url="http://localhost:11434/v1"), mode=instructor.Mode.JSON)
    @component.output_types(report=str)
    def run(self, query: str):
        report = model_response(query)
        return {"report": report}
