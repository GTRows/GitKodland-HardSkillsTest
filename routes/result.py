from flask import Blueprint, render_template, request, redirect, url_for, session
from models.question import Question
import json

result_bp = Blueprint('result', __name__)

@result_bp.route('/result', methods=['POST'])
def result():
    score = 0
    user_answers = request.form

    with open('resources/questions.json', 'r') as f:
        questions_data = json.load(f)
    questions = [Question(**question) for question in questions_data]

    for question in questions:
        user_answer = user_answers.get(question.name)
        if question.answer is not None:
            if question.type == 'radio' and user_answer == question.answer:
                score += 1
            elif question.type == 'text' and user_answer.lower() == question.answer.lower():
                score += 1

    session['score'] = score
    best_score = session.get('best_score', 0)
    if score > best_score:
        session['best_score'] = score
        best_score = score

    return render_template('result.html', score=score, best_score=best_score)