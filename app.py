from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions = [
    {
        'question': 'What is your name?',
        'type': 'text',
        'name': 'username',
        'answer': None
    },
    {
        'question': 'What is your favorite color?',
        'type': 'radio',
        'name': 'question1',
        'options': ['red', 'blue', 'green'],
        'answer': 'blue'
    },
    {
        'question': 'What is your favorite animal?',
        'type': 'radio',
        'name': 'question2',
        'options': ['dog', 'cat', 'parrot'],
        'answer': 'dog'
    },
    {
        'question': 'Describe your hobbies or interests:',
        'type': 'textarea',
        'name': 'question3',
        'answer': None
    }
]


@app.route('/')
def index():
    return render_template('index.html', questions=questions)


@app.route('/result', methods=['POST'])
def result():
    score = 0
    user_answers = request.form
    print(user_answers)
    print(questions)
    for i, question in enumerate(questions):
        user_answer = user_answers.get(question['name'])
        if question['answer'] is not None:
            if question['type'] == 'radio' and user_answer == question['answer']:
                score += 1
            elif question['type'] == 'text' and user_answer.lower() == question[
                'answer'].lower():
                score += 1

    session['score'] = score
    best_score = session.get('best_score', 0)
    if score > best_score:
        session['best_score'] = score
        best_score = score

    return render_template('result.html', score=score, best_score=best_score)


if __name__ == '__main__':
    app.run(debug=True)
