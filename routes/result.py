from flask import Blueprint, render_template, request, redirect, url_for, session
from models.question import Question
from models.database import Database

result_bp = Blueprint('result', __name__)

db = Database.get_instance()

@result_bp.route('/result', methods=['POST'])
def result():
    score = 0
    user_answers = request.form

    questions = []
    for row in db.get_questions():
        questions.append(Question.from_db(row))
        print(f"Questions results: {questions}")

    for question in questions:
        user_answer = user_answers.get(question.name)
        if question.answer is not None:
            if question.type == 'radio' and user_answer == question.answer:
                score += 1
            elif question.type == 'text' and user_answer.lower() == question.answer.lower():
                score += 1

    session['score'] = score

    db.log_result(user_id=1, score=score, answers=user_answers)

    return render_template('result.html', score=score, best_score=best_score)