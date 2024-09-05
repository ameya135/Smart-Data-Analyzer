import instructor
from pydantic import BaseModel

class QueryFormat(BaseModel):
    query: str


