from models.base_object import BaseObject


class Student(BaseObject):
    def __init__(self, first_name, last_name, student_id, **kwargs):
        super().__init__(first_name=first_name, last_name=last_name, student_id=student_id, **kwargs)
