from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.question import Question
from servies.database import Database
import re

main_bp = Blueprint('main', __name__)

db = Database.get_instance()


@main_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_id = request.form.get('studentid')
        if student_id and not re.match("^[0-9]{8}$", student_id):
            flash("Please enter a valid student ID.", 'error')
            return render_template('index.html')
        if student_id:
            user = db.get_user_by_id(student_id)
            if user:
                flash(f"Hoş geldin {user['name']} {user['surname']}", 'success')
                session['user_id'] = user['id']
                return redirect(url_for('main.quiz'))
            else:
                session['studentid'] = student_id
                flash("Öğrenci bulunamadı. Lütfen kayıt olun.", 'error')
                return redirect(url_for('main.register'))
        else:
            flash("Lütfen öğrenci ID'nizi girin.", 'error')
            return render_template('index.html')
    else:
        return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    studentid = session.get('studentid')

    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')

        if name and surname:
            db.register_user(studentid, name, surname)
            flash("Kayıt başarılı.", 'success')
            session['user_id'] = db.get_user_by_id(studentid)['id']
            return redirect(url_for('main.quiz'))
        else:
            flash("Lütfen tüm alanları doldurun.", 'error')
            return render_template('register.html', studentid=studentid)
    else:
        return render_template('register.html', studentid=studentid)
@main_bp.route('/quiz')
def quiz():
    user_id = session.get('user_id')
    if user_id:
        questions = db.get_questions()
        best_score = db.get_user_best_score(user_id)
        return render_template('quiz.html', questions=questions, best_score=best_score)
    else:
        flash("Lütfen önce giriş yapın.", 'error')
        return redirect(url_for('main.index'))