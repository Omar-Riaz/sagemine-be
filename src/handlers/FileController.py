from flask import Blueprint, request, Response
from flask.views import MethodView
from services.embeddings.EmbeddingService import EmbeddingService

file_controller = Blueprint('file_controller', __name__)


class FileController(MethodView):
    def __init__(self) -> None:
        self.embeddingService = EmbeddingService()

    def post(self):
        if 'file' not in request.files:
            return 'No file passed in request', 400
        file = request.files['file']
        source = "curriculum"
        course = "TM101"
        self.embeddingService.compute_and_store_embeddings(file, source, course)
        return "File successfully parsed", 200

# NOTE: view_func is the function that will be called when the route is matched. 
file_controller.add_url_rule('/upload', view_func=FileController.as_view('upload_file'), methods=['POST'])
