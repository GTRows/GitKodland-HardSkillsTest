from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.question import Question
from servies.database import Database
import re

result_bp = Blueprint('result', __name__)

db = Database.get_instance()


@result_bp.route('/result', methods=['POST'])
def result():
    score = 0
    user_answers = request.form

    questions = db.get_questions()

    for question in questions:
        user_answer = user_answers.get(question['name'])
        print(question)
        if question['answer'] is not None:
            if question['type'] == 'textarea':
                continue
            elif question['type'] == 'radio' and user_answer == question['answer']:
                score += int(question['points'])
            elif question['type'] == 'text' and user_answer.lower() == question['answer'].lower():
                score += int(question['points'])

    user_id = session.get('user_id')
    if user_id:
        best_score = db.get_user_best_score(user_id)
        if best_score is None:
            best_score = 0
        if score > best_score:
            best_score = score
        db.log_result(user_id=user_id, score=score, answers=user_answers)
        return render_template('result.html', score=score, best_score=best_score)
    else:
        flash("Lütfen önce giriş yapın.", 'error')
        return redirect(url_for('main.index'))
