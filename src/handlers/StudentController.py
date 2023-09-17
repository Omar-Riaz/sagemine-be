from flask import Blueprint, request, Response
from flask.views import MethodView
from daos.StudentDao import StudentDao
from flask import jsonify
from email_validator import validate_email, EmailNotValidError


student_controller = Blueprint('student_controller', __name__)


class AddStudentController(MethodView):
    def __init__(self) -> None:
        self.student_dao = StudentDao()

    def post(self):
        if 'email' not in request.json:
            return 'No user email provided', 400
        email = request.json['email']
        try:
            validate_email(email)
        except EmailNotValidError as err:
            return jsonify({'error': str(err)}), 400
        course = "TM101"
        self.student_dao.insert_student(email=email, course=course)
        return "Student successfully added", 200


class AddSuggestionsController(MethodView):
    def __init__(self) -> None:
        self.student_dao = StudentDao()

    def get(self, id: str):
        try:
            return jsonify(self.student_dao.get_suggestions(id=id)), 200
        except self.student_dao.NoStudentFoundException as err:
            print(jsonify({'error': str(err)}))
            return jsonify({'error': str(err)}), 404
        except Exception as err:
            print(jsonify({'error': str(err)}))
            return jsonify({'error': str(err)}), 500
        


student_controller.add_url_rule('/student', view_func=AddStudentController.as_view('add_student'), methods=['POST'])
student_controller.add_url_rule('/student/<id>/suggestions', view_func=AddSuggestionsController.as_view('get_suggestions'), methods=['GET'])
