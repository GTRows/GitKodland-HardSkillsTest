import uuid

class BaseObject:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', str(uuid.uuid4()))
        for key, value in kwargs.items():
            if key != 'id':
                setattr(self, key, value)

    @classmethod
    def from_db(cls, row_dict):
        id = row_dict.pop('id', None)
        return cls(id=id, **row_dict)

    def print_all(self):
        attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return ", ".join(attributes)