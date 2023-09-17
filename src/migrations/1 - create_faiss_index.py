from pymongo import MongoClient
from bson.binary import Binary
import faiss
import pickle

def run_migration():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["sagemine"]
    collection = db["embeddings"]
    if collection.count_documents({'_id': 'serialized_faiss_index'}) > 0:
        print("FAISS index already exists, replacing")
        collection.delete_many({'_id': 'serialized_faiss_index'})
    faiss_index = faiss.IndexFlatL2(384)
    serialized_faiss_index = Binary(pickle.dumps(faiss.serialize_index(faiss_index)))
    collection.insert_one({'_id': 'serialized_faiss_index', 'faiss_index': serialized_faiss_index})
    print("FAISS index created successfully.")

if __name__ == "__main__":
    run_migration()
