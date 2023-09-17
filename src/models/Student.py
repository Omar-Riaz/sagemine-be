from pydantic import BaseModel

class Student(BaseModel):
    course: str
    email: str
    suggestions: dict[str, int]

