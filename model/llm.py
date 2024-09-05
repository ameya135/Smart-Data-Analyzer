import instructor
from pydantic import BaseModel, Field
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY")

class QueryFormat(BaseModel):
    query: str = Field(None, alias="Postgres Query.")
    suggestion: str = Field(None, alias="Suggest any changes that can be made to the query. Return None if there are no suggestions.")

def model_response(query:str):

    client = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    completion = client.messages.create(
      response_model=QueryFormat,
      messages=[
        {"role": "user",
         "content": f"I want the postgres query for the given statement: {query}"
        },
      ],
      temperature=0.7,
    )

    return completion.model_dump_json(indent=2)

#query = "Names of all employees that have minimum salary of 199999 and order them by their city name."
#print(model_response(query))
