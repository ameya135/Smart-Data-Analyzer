import pydantic


class QueryProcessorResponseModel(pydantic.BaseModel):
    database_query: str


class QueryCheckerResponseModel(pydantic.BaseModel):
    user_prompt: str
    database_query: str
    database_output: str
    isValid: bool
