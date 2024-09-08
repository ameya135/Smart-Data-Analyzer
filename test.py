import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyBHYovQe-6aJY7y2myXgSUt6hnK0XKxoco")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(
    "I want the postgres query for the given statement: Names of all employees that have minimum salary of 199999 and order them by their city name."
)
print(response.text)
