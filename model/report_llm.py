import os

import google.generativeai as genai
import instructor
from pydantic import BaseModel, Field

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def report_model_response(report_prompt: str, response_model_class: str):

    client = instructor.from_gemini(
        client=genai.GenerativeModel(
            model_name="models/gemini-1.5-flash-latest",
        ),
        mode=instructor.Mode.GEMINI_JSON,
    )
    completion = client.messages.create(
        response_model=response_model_class,
        messages=[
            {
                "role": "user",
                "content": report_prompt,
            },
        ],
        temperature=0.7,
    )

    return completion.model_dump_json(indent=2)


# query = "Names of all employees that have minimum salary of 199999 and order them by their city name."
# print(model_response(query))
