from pymongo import MongoClient
from bson.binary import Binary
import faiss
import numpy as np
from typing import List, Union
import pickle
from models.Embedding import Embedding


class EmbeddingDao:
    def __init__(self, uri='mongodb://localhost:27017/', db_name='sagemine', collection_name='embeddings'):
        print("Initializing EmbeddingDao")
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def add_embeddings(self, source: str, course: str, sentences: List[str], embeddings: List[Union[np.ndarray, List[List[float]]]]):
        
        if self.collection.count_documents({'_id': 'serialized_faiss_index'}) > 0:
            print("FAISS index already exists")
        else:
            faiss_index = faiss.IndexFlatL2(384)
            serialized_faiss_index = Binary(pickle.dumps(faiss.serialize_index(faiss_index)))
            self.collection.insert_one({'_id': 'serialized_faiss_index', 'faiss_index': serialized_faiss_index})
            print("FAISS index created successfully.")
        

        documents = []
        faiss_index_doc = self.collection.find_one({'_id': "serialized_faiss_index"})

        faiss_index = faiss.deserialize_index(pickle.loads(faiss_index_doc['faiss_index']))
        curr_faiss_vec_num = faiss_index.ntotal  # Gets the current number of vectors in the index

        for sentence, embedding in zip(sentences, embeddings):
            print("adding sentence", sentence)
            documents.append({
                'course': course,
                'source': source,
                'sentence': sentence,
                'embedding': embedding.tolist() if isinstance(embedding, np.ndarray) else embedding,
                'vec_num': curr_faiss_vec_num,  # Adds the Faiss index as a new field
            })
            embedding_np = np.array(embedding).reshape(1, -1)
            faiss.normalize_L2(embedding_np)
            faiss_index.add(embedding_np)
            curr_faiss_vec_num += 1  # Increments the Faiss index for the next vector

        self.collection.insert_many(documents)
        faiss_index_binary = Binary(pickle.dumps(faiss.serialize_index(faiss_index)))
        self.collection.update_one({'_id': "serialized_faiss_index"}, {'$set': {'faiss_index': faiss_index_binary}})



    def get_closest_embeddings(self, prompt_embedding: np.ndarray, closest_embedding_count: int) -> List[Embedding]:
        faiss.normalize_L2(prompt_embedding)
        index_doc = self.collection.find_one({'_id': "serialized_faiss_index"})
        print("index_doc", index_doc)
        index = faiss.deserialize_index(pickle.loads(index_doc['faiss_index']))
        _, indexes = index.search(prompt_embedding.reshape(1,-1), closest_embedding_count)
        indexes_list = [x.item() for x in indexes[0]]
        result = self.collection.find({'vec_num': {'$in': indexes_list}})
        return list(result)