from werkzeug.datastructures import FileStorage
import nltk
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from daos.EmbeddingDao import EmbeddingDao


class EmbeddingService:
    def __init__(self) -> None:
        nltk.download('punkt')
        self.embeddingDao = EmbeddingDao()

    def split_into_sentences(self, text: str) -> list[str]:
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
        sentences = sent_detector.tokenize(text.strip())
        return sentences

    def compute_and_store_embeddings(self, file: FileStorage, source: str, course: str):
        pdf = PdfReader(file)
        text = ''
        for page_num in range(max(20, len(pdf.pages))):
            text += pdf.pages[page_num].extract_text()
        sentences = self.split_into_sentences(text)
        model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        sentence_embeddings = model.encode(sentences)
        self.embeddingDao.add_embeddings(source, course, sentences, sentence_embeddings)


        


