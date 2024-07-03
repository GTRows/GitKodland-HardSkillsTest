import sqlite3
import json
import os

class Database:
    __instance = None

    @staticmethod
    def get_instance(db_file="quiz.db"):
        if Database.__instance is None:
            db = Database(db_file)
        return Database.__instance

    def __init__(self, db_file="quiz.db"):
        if Database.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.setup()
            self.db_file = db_file
            self.conn = None
            self.cursor = None
            Database.__instance = self

    def connect(self, db_file="quiz.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()

    def setup(self, db_file="quiz.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT,
                    type TEXT,
                    name TEXT,
                    points INTEGER,
                    options TEXT,
                    answer TEXT,
                    required BOOLEAN
                )
            """)
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    score INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS answers (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            result_id INTEGER,
                            question_name TEXT,
                            answer TEXT
                        )
                    """)
        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            student_id TEXT UNIQUE,
                            name TEXT,
                            surname TEXT
                        )
                    """)
        self.conn.commit()
        self.load_questions()

    def load_questions(self):
        self.cursor.execute("SELECT COUNT(*) FROM questions")
        if self.cursor.fetchone()[0] > 0:
            return
        file_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'questions.json')

        with open(file_path, 'r') as f:
            questions_data = json.load(f)

        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                type TEXT,
                name TEXT,
                points INTEGER,
                options TEXT,
                answer TEXT,
                required BOOLEAN
            )
        """)

        for question in questions_data:
            options_str = ",".join(question.get('options', []))
            cursor.execute("""
                INSERT INTO questions (question, type, name, points, options, answer, required)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (question['question'], question['type'], question['name'],question['points'], options_str, question.get('answer'),
                  question['required']))
        conn.commit()

    def get_questions(self):
        if self.cursor is None:
            self.connect()
        self.cursor.execute("SELECT * FROM questions")
        rows = self.cursor.fetchall()
        questions = []
        for row in rows:
            question_data = dict(zip([column[0] for column in self.cursor.description], row))
            question_data['options'] = question_data['options'].split(',') if question_data.get('options') else []
            questions.append(question_data)
        return questions

    def get_user_by_id(self, student_id):
        self.cursor.execute("SELECT * FROM users WHERE student_id = ?", (student_id,))
        user = self.cursor.fetchone()
        if user:
            return dict(zip([column[0] for column in self.cursor.description], user))
        return None

    def register_user(self, student_id, name, surname):
        self.cursor.execute(
            "INSERT INTO users (student_id, name, surname) VALUES (?, ?, ?)",
            (student_id, name, surname)
        )
        self.conn.commit()

    def log_result(self, user_id, score, answers):
        if self.cursor is None:
            self.connect()
        self.cursor.execute(
            "INSERT INTO results (user_id, score) VALUES (?, ?)",
            (user_id, score)
        )
        self.conn.commit()

        result_id = self.cursor.lastrowid

        for question_name, answer in answers.items():
            self.cursor.execute(
                "INSERT INTO answers (result_id, question_name, answer) VALUES (?, ?, ?)",
                (result_id, question_name, answer)
            )
        self.conn.commit()

    # Kodu optimize et
    def get_user_best_score(self, user_id) -> int:
        self.cursor.execute("SELECT MAX(score) FROM results WHERE user_id = ?", (user_id,))
        best_score = self.cursor.fetchone()
        if best_score:
            return best_score[0]
        else:
            return -1

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
