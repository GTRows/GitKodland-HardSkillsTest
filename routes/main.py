from flask import Blueprint, render_template
from models.question import Question
from servies.database import Database
import re

main_bp = Blueprint('main', __name__)

db = Database.get_instance()


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    questions = []
    for row in db.get_questions():
        questions.append(Question.from_db(row))
    for question in questions:
        print(question.print_all())
        attrs = vars(question)
        print(', '.join("%s: %s" % item for item in attrs.items()))

    return render_template('index.html', questions=questions)
