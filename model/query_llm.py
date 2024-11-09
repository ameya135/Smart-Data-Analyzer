import os
import pydantic
import instructor
from pydantic import BaseModel, Field
from openai import OpenAI

class QueryCheckerResponseModel(pydantic.BaseModel):
    user_prompt: str
    database_query: str
    database_output: str
    isValid: bool


def model_response(response_model_class: str, prompt: str):

    client = instructor.from_openai(
        OpenAI(base_url="https://2db8-34-82-155-86.ngrok-free.app/v1", api_key="12345678")
        )
    completion = client.chat.completions.create(
        response_model=response_model_class,
        messages=[
            {
                "role": "user",
                "content": prompt
            },
        ],
        temperature=0.7,
        model="Veer15/Llama3_1Text2Sql"
    )

    return completion.model_dump_json(indent=2)


query = "Names of all employees that have minimum salary of 199999 and order them by their city name."
print(model_response(prompt=query, response_model_class=QueryCheckerResponseModel))
