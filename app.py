from flask import Flask, render_template, request, redirect, url_for, session
from routes.main import main_bp
from routes.result import result_bp
from models.question import Question  # Soru modelini import et

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Yolları kaydet
app.register_blueprint(main_bp)
app.register_blueprint(result_bp)

if __name__ == '__main__':
    app.run(debug=True)