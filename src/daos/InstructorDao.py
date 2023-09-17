from pymongo import MongoClient
from typing import Optional
from models.Instructor import Instructor


class InstructorDao:
    def __init__(self, uri: str, db_name: str, collection_name: str) -> None:
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert_instructor(self, instructor: Instructor) -> None:
        instructor_dict = {
            'id': instructor.id,
            'name': instructor.name,
            'saved_files': instructor.saved_files
        }
        self.collection.insert_one(instructor_dict)

    def find_instructor(self, id: str) -> Optional[Instructor]:
        result = self.collection.find_one({'id': id})
        if result is not None:
            return Instructor(result['name'], result['id'], result['saved_files'])
        return None

    def delete_instructor(self, id: str) -> None:
        self.collection.delete_one({'id': id})
