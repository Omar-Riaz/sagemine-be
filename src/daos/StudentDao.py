from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Optional
from models.Student import Student
from collections import Counter

class StudentDao:

    class NoStudentFoundException(Exception):
        pass

    def __init__(self,uri='mongodb://localhost:27017/', db_name='sagemine', collection_name='students') -> None:
        print("Initializing student dao")
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_student(self, email, course) -> None:
        student_dict = {
            'email': email,
            'course': course
        }
        self.collection.insert_one(student_dict)

#TODO: is this approach scalable? Better to use kwargs in model constructor? Concern with field lenience?
    def find_student_by_email(self, email: str) -> Optional[Student]:
        result = self.collection.find_one({'email': email})
        if result:
            return Student(email=result['email'], course=result['course'], suggestions=result['suggestions'])
        return None

    def delete_student(self, id: str) -> None:
        self.collection.delete_one({'id': id})

    def add_suggestions(self, id:str, sources: list[str]) -> bool:
        """
        Adds a list of suggestions to the student with the given id

        Raises: NoStudentFoundException if no student with the given id is found
        """
        source_counts = Counter(sources)
        # print(source_counts)
        update_fields = {f'suggestions.{source}': count for source, count in source_counts.items()}
        result = self.collection.update_one({'_id': ObjectId(id)}, {'$inc': update_fields})
        if result.modified_count == 0:
            self.collection.insert_one({'_id': ObjectId(id), 'suggestions': source_counts})
            # raise self.NoStudentFoundException(f"No student with id {id} found")

        
    def get_suggestions(self, id: str) -> list[str]:
        """
        Returns the list of suggestions to the student with the given id

        Raises: NoStudentFoundException if no student with the given id is found
        """
        result = self.collection.find_one({'_id': ObjectId(id)})
        if not result:
            print(f"No student with id {id} found")
            raise self.NoStudentFoundException(f"No student with id {id} found")
        if not result['suggestions']:
            print(f"No suggestions for student {id} found")
            raise self.NoStudentFoundException(f"No suggestions for student {id} found")
        return result['suggestions']