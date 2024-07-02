import json

from flask import Blueprint, render_template
from models.question import Question

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    with open('resources/questions.json', 'r') as f:
        questions_data = json.load(f)

    questions = [Question(**question) for question in questions_data]

    return render_template('index.html', questions=questions)
