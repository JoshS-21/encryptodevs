from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"User({self.id}, {self.name}, {self.email}, {self.password})"

