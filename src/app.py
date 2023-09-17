from flask import Flask
from flask_cors import CORS
from handlers.FileController import file_controller
from handlers.PromptController import prompt_controller 
from handlers.StudentController import student_controller

app = Flask(__name__)
CORS(app)

app.register_blueprint(file_controller, url_prefix='/api')  # Register the blueprint with your application
app.register_blueprint(prompt_controller, url_prefix='/api')  # Register the blueprint with your application
app.register_blueprint(student_controller, url_prefix='/api')  # Register the blueprint with your application