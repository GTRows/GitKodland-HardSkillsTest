from flask import Flask, render_template, request, redirect, url_for, session, flash
from routes.main import main_bp
from routes.result import result_bp
from models.database import Database

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.register_blueprint(main_bp)
app.register_blueprint(result_bp)

db = Database.get_instance()

@app.teardown_appcontext
def close_connection(exception):
    global db
    if db is not None:
        db.close()

@app.before_request
def before_request():
    global db
    db = Database.get_instance()
    if db.conn is None:
        db.connect()

if __name__ == '__main__':
    app.run(debug=True)
