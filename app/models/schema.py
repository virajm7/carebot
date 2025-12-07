from pydantic import BaseModel

class Query(BaseModel):
    query: str

class Answer(BaseModel):
    response: str
