from servies.database import Database


# implement base object
class Question:
    def __init__(self, id, question, question_type, name, points, options=None, answer=None, required=False):
        self.id = id
        self.question = question
        self.type = question_type
        self.name = name
        self.points = points
        self.options = options
        self.answer = answer
        self.required = required

    @classmethod
    def from_db(cls, row_dict):
        return cls(row_dict['question'], row_dict['type'], row_dict['name'],row_dict['points'], row_dict['options'], row_dict['answer'],
                   row_dict['required'])

    def print_all(self):
        return f"Question: {self.question}, Type: {self.type}, Name: {self.name}, Points: {self.points},Options: {self.options}, Answer: {self.answer}, Required: {self.required}"
