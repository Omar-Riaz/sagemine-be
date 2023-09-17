from InstructorDao import InstructorDao
from pymongo import MongoClient
from injector import Module, Binder, singleton
from config import Config

class DaoModule(Module):
    def configure(self, binder: Binder):
        binder.bind(
            InstructorDao, 
            to=InstructorDao(
                MongoClient(Config.DB_URI), 
                Config.DB_NAME, 
                Config.COLLECTION_NAME
            ), 
            scope=singleton
        )