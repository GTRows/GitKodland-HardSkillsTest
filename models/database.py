import sqlite3
import json


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
                    best_score INTEGER,
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
        self.conn.commit()
        self.load_questions()

    def load_questions(self):
        self.cursor.execute("SELECT COUNT(*) FROM questions")
        if self.cursor.fetchone()[0] > 0:
            return

        with open('resources/questions.json', 'r') as f:
            questions_data = json.load(f)

        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                type TEXT,
                name TEXT,
                options TEXT,
                answer TEXT,
                required BOOLEAN
            )
        """)

        for question in questions_data:
            options_str = ",".join(question.get('options', []))
            cursor.execute("""
                INSERT INTO questions (question, type, name, options, answer, required)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (question['question'], question['type'], question['name'], options_str, question.get('answer'),
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

    def log_result(self, user_id, score, best_score, answers):
        if self.cursor is None:
            self.connect()
        self.cursor.execute(
            "INSERT INTO results (user_id, score, best_score) VALUES (?, ?, ?)",
            (user_id, score, best_score)
        )
        self.conn.commit()

        for question_name, answer in answers.items():
            self.cursor.execute(
                "INSERT INTO answers (result_id, question_name, answer) VALUES (?, ?, ?)",
                (self.cursor.lastrowid, question_name, answer)
            )
        self.conn.commit()

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
