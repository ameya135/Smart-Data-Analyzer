import os
import sys
from typing import Optional

import google.generativeai as genai
import instructor
import pydantic
from haystack import component
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.postgres import PostgresDB
from model.query_llm import model_response
from prompts import (
    create_query_processor_prompt_initial,
    create_query_processor_prompt_not_valid,
)


class QueryProcessorResponseModel(BaseModel):
    database_query: str


@component
class QueryProcessor:
    """
    A component to process the query and return the result.
    Output:
        db_output: str
        query: str
        natural_language: str
    """

    client = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )

    @component.output_types(db_output=str, db_query=str, natural_language=str)
    def run(
        self,
        natural_language: str,
        db_query: Optional[str] = None,
        valid: Optional[bool] = None,
        db_output: Optional[str] = None
    ):
        try:
            prompt = create_query_processor_prompt_initial(natural_language)

            if valid is not None and not valid:
                prompt = create_query_processor_prompt_not_valid(
                    natural_language, db_query
                )

            db_query = model_response(
                response_model_class=QueryProcessorResponseModel,
                prompt=prompt,
            ).database_query

            db_output = None
            if query:
                with PostgresDB() as db:
                    db_output = db.run_sql(query)

            return {
                "db_output": db_output,
                "query": db_query,
                "natural_language": natural_language,
            }
        except Exception as e:
            return {
                "db_output": None,
                "query": None,
                "natural_language": natural_language,
                "error": str(e),
            }
