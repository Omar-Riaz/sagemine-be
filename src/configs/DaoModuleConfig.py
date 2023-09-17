import os

class Config:
    DB_URI = os.getenv('DB_URI', 'mongodb://localhost:27017')
    DB_NAME = os.getenv('DB_NAME', 'sagemine')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'instructors')