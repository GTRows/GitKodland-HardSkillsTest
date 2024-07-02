class BaseObject:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_db(cls, row_dict):
        return cls(**row_dict)

    def print_all(self):
        attributes = [f"{key}: {value}" for key, value in self.__dict__.items()]
        return ", ".join(attributes)
