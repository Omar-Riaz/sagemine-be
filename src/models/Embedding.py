from pydantic import BaseModel

class Embedding(BaseModel):
    sentence: str
    embedding: float
    source: str
    course: str
    insertion_order: int
