import os
import sys
from typing import Optional

import instructor
from haystack import component
from openai import OpenAI
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from types import QueryProcessorResponseModel

from database.postgres import PostgresDB
from model.query_llm import model_response
from prompts import (
    create_query_processor_prompt_initial,
    create_query_processor_prompt_not_valid,
)


@component
class QueryProcessor:
    """
    A component to process the query and return the result.
    Output:
        sql_query: str
        data: dict
        user_query: str
    """

    client = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )

    @component.output_types(db_output=str, query=str, natural_language=str)
    def run(
        self,
        natural_language: str,
        db_query: str,
        valid: Optional[bool] = None,
    ):
        prompt = create_query_processor_prompt_initial(natural_language)
        if valid is not None:
            prompt = create_query_processor_prompt_not_valid(natural_language, db_query)
        query = model_response(
            response_model_class=QueryProcessorResponseModel,
            prompt=prompt,
        )
        with PostgresDB() as db:
            db_output = db.run_sql(query)

        return {
            "db_output": db_output,
            "query": query,
            "natural_language": natural_language,
        }
