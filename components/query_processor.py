import os
import sys

import instructor
from haystack import component
from openai import OpenAI
from pydantic import BaseModel

from model.llm import model_response

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class QueryFormat(BaseModel):
    query: str


@component
class QueryProcessor:
    """
    A component to process the query and return the result.
    Output:
        sql_query: str
        data: dict
        user_query: str
    """

    client = instructor.from_openai(
        OpenAI(api_key="ollama", base_url="http://localhost:11434/v1"),
        mode=instructor.Mode.JSON,
    )

    @component.output_types(report=str)
    def run(self, query: str):
        report = model_response(query)
        return {"report": report}
