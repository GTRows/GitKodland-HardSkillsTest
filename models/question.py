class Question:
    def __init__(self, question, type, name, options=None, answer=None, required=False):
        self.question = question
        self.type = type  # Bu doğru olmalı
        self.name = name
        self.options = options
        self.answer = answer
        self.required = required