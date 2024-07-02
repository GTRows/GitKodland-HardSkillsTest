from models.base_object import BaseObject

class Question(BaseObject):
    def __init__(self, question, question_type, name, points, options=None, answer=None, required=False, **kwargs):
        super().__init__(question=question, question_type=question_type, name=name, points=points,
                         options=options, answer=answer, required=required, **kwargs)