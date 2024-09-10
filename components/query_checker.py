import os
import sys
import pydantic

import instructor
from haystack import component
from openai import OpenAI
from pydantic import BaseModel

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from database.postgres import PostgresDB
from model.query_llm import model_response
from prompts import create_query_checker_prompt


class QueryCheckerResponseModel(pydantic.BaseModel):
    user_prompt: str
    database_query: str
    database_output: str
    isValid: bool

@component
class QueryChecker:
    """
    A component to check if the query is valid. If not valid, send a suggestion back.
    Else, forward the query to the next component.
    """

    @component.output_types(valid=str, response=str, db_response=str)
    def run(self, db_output: str, query: str, natural_language: str):
        response_check = model_response(
            response_model_class=QueryCheckerResponseModel,
            prompt=create_query_checker_prompt(
                db_output=db_output, db_query=query, user_prompt=natural_language
            ),
        )
        return {
            "response": response_check,
            "valid": response_check.isValid,
            "db_response": response_check.database_output,
        }
