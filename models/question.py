from models.base_object import BaseObject


class Question(BaseObject):
    def __init__(self, question, question_type, name, options=None, answer=None, required=False):
        super().__init__(question=question, type=question_type, name=name, options=options, answer=answer,
                         required=required)
