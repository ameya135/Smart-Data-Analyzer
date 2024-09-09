
import os
import sys

import instructor
from haystack import component
from openai import OpenAI
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from model.query_llm import model_response
from database.postgres import PostgresDB


class QueryFormat(BaseModel):
    natural_language: str


@component
class ReportGenerator:
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

    @component.output_types(db_output=str)
    def run(self, natural_language: str):
        query = model_response(natural_language)
        with PostgresDB() as db:
            db_output = db.run_sql(query)

        return {"db_output": db_output}
