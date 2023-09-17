from typing import Optional
from pydantic import BaseModel

class Sentence(BaseModel):
    source: Optional[str]
    string: str
    isDiagram: bool